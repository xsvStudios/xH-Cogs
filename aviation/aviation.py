import discord
from redbot.core import commands, checks, Config

from datetime import datetime
from time import time
import json
import os
import requests


class Aviation(commands.Cog):
    """
        Has some simple aviation commands such as checking for airport weather, tracking planes, etc...
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 127481152069)
        default_guild = {
            'aviationApiKey': None
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.is_owner()
    async def setapikey(self, ctx: commands.Context, key: str) -> None:
        """
            Sets token to be used with avwx.rest
            You can get it from https://avwx.rest/
            This is to get data from METAR and other types of data.
        """
        

        # TODO: Make this DM only for extra security

        # Check key length
        if len(key) != 43:
            return await ctx.send('Your api key is not the correct length. Please try again with a correct key.')

        # Set the api key
        await self.config.guild(ctx.guild).aviationApiKey.set(key)
        await ctx.send('Credentials set.')

        # Delete the message sent by the user if we can so we don't have the api key just sitting there
        if ctx.channel.permissions_for(ctx.me).manage_messages:
            return await ctx.message.delete()
        else:
            return await ctx.send('I\'m not able to delete that message, please do so to keep your key safe.')


    def airportLookup(self, airport_code: str, airport_code_type: str):
        """
            Loads the airport lookup table from airports.json and loads it into memory.
            Searches the lookup file for the specefied ICAO or IATA code and returns the hit if found.
            TODO: Make this more efficient by loading it only once in the __init__ of the cog so we don't waste time loading it again.
        """

        try:
            # Open local JSON file
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'airports.json') , 'r', encoding='utf-8') as f:
                airport_obj = json.load(f)
            
            # Search the json list for a match
            # (doing it the long way because that's how the dataset is, and because of the complexity of 2 possible lookups per query)
            if airport_obj != None:
                if len(airport_obj) > 0:
                    for x in airport_obj:
                        if airport_code_type == 'ICAO':
                            # ICAO -> 4 letters
                            if 'icao' in airport_obj[x]:
                                if airport_obj[x]['icao'].upper() == airport_code.upper():
                                    # Match found, return x
                                    return airport_obj[x]
                        
                        elif airport_code_type == 'IATA':
                            # IATA -> 3 letters
                            if 'iata' in airport_obj[x]:
                                if airport_obj[x]['iata'].upper() == airport_code.upper():
                                    # Match found, return x
                                    return airport_obj[x]

            # Match wasn't found...
            return None
        except:
            # Something blew up?
            return None

        return None

    def getMetarInfo(self, icao_code: str, apikey: str):
        """
            Calls an api that fetches METAR weather info from an input ICAO airport code.
            Returns back the info for that requested airport if possible.

            TODO: Implement proper api error handling here
        """
        
        # Define api call url
        apiurl = f'https://avwx.rest/api/metar/{icao_code}?options=&airport=true&reporting=true&format=json&onfail=cache'

        # TODO: REMOVE WHEN IT WORKS
        print(f'apiurl: {apiurl}\napikey: {apikey}')

        try:
            # Do the api call
            response = requests.get(apiurl, headers={ 'Authorization': f'Bearer {apikey}' })

            # Make sure it went well...
            if response.status_code != 200:
                # TODO: REMOVE WHEN IT WORKS
                print(response.text)
                return None

            print(response.json())
            return response.json()

        except Exception as e:
            # TODO: REMOVE WHEN IT WORKS
            print(e)
            return None

    @commands.command()
    async def metar(self, ctx, station_id: str):
        """
            Gets the current weather information from a specified airport IATA or ICAO airport code.

            General list of airports with IATA and ICAO codes: https://en.wikipedia.org/wiki/Lists_of_airports
            **ICAO** Codes (4 letters): https://en.wikipedia.org/wiki/ICAO_airport_code
            **IATA** Codes (3 letters): https://en.wikipedia.org/wiki/IATA_airport_code
            
            Will return the data in an embed to the user with useful weather information of the airport.

            **Example**:
            ```css
            [ICAO]
            [p]metar kord
            ```
            ```css
            [IATA]
            [p]metar aaa
            ```
        """

        # Checks to see if the input string is a ICAO or IATA input
        if (not station_id.isalpha()) or (len(station_id) not in [3, 4]):
            return await ctx.send(f'Your input must be an ICAO or IATA code. Get more info by typing: **{ctx.prefix}help {ctx.command}**')

        # Check if our api key exists/is valid before we do anything...
        apikey = await self.config.guild(ctx.guild).aviationApiKey()
        if (apikey == None) or (len(apikey) != 43):
            return await ctx.send(f'Your api key isn\'t set just yet. Please run **{ctx.prefix}help setapikey** for more information. (only the owner can set this)')

        """
            Check to see if the airport code exists, if it does, get some info and pass it along to the api.
        """

        # Start performance timer
        start_time = time()

        # Define global object to assign in the case types below
        station_obj = None

        if len(station_id) == 4:
            # ICAO Code handling

            # Lookup ICAO code and return object if found
            icao_lookup = self.airportLookup(station_id, 'ICAO')
            if icao_lookup == None:
                return await ctx.send(f'Error: The airport ICAO code with input ID \'**{station_id}**\' was not found!')

            # Lookup was successful
            station_obj = icao_lookup
        elif len(station_id) == 3:
            # IATA Code handling

            # Lookup IATA code and return object if found
            iata_lookup = self.airportLookup(station_id, 'IATA')
            if iata_lookup == None:
                return await ctx.send(f'Error: The airport IATA code with input ID \'**{station_id}**\' was not found!')

            # Lookup was successful
            station_obj = iata_lookup
        else:
            # If this gets hit, then it somehow avoided the filters? How???
            return await ctx.send(f'Your input must be an ICAO or IATA code. Get more info by typing: **{ctx.prefix}help {ctx.command}**')

        # Exit if something bad happened. (over-engineering, but whatever)
        if station_obj is None:
            return await ctx.send('An error occured looking up your airport code. Please try again or try a different code.')

        try:
            # Parse out the response we got and get out the info into variables we can use
            airport_icao_code = station_obj['icao']
            airport_iata_code = station_obj['iata']
            airport_name = station_obj['name']
            airport_city = station_obj['city']
            airport_state = station_obj['state']
            airport_country = station_obj['country']
            # airport_elevation = station_obj['elevation']
            # airport_latitude = station_obj['lat']
            # airport_longitude = station_obj['lon']
            # airport_timezone = station_obj['tz']

            # End performance timer for lookup
           #  elapsed_time_in_ms_for_lookup = '{0:.2f}'.format(((time() - start_time) * 1000))

            """
                Perform API call to actually get metar weather information.
            """
            apiResponse = self.getMetarInfo(airport_icao_code.upper(), apikey)
            print(f'apiresponse: {apiResponse}')
            if apiResponse == None:
                return await ctx.send('It seems like the api call has failed to get the METAR information. Please try again later.')
            
            metar_meta = apiResponse['meta'] # timestamp, stations_updated, and cache-timestamp (datetime)
            metar_altimeter = apiResponse['altimeter'] # repr, value, spoken
            metar_clouds = apiResponse['clouds'] # Array of objects, each containing: repr, type, altitude (* 100 for alt), modifier, direction
            # metar_other = apiResponse['other']
            metar_flight_rules = apiResponse['flight_rules']
            metar_sanatized_str = apiResponse['sanitized']
            metar_visibility = apiResponse['visibility'] # repr, value, spoken
            metar_wind_dir = apiResponse['wind_direction'] # repr, value, spoken
            # metar_wind_variable_direction = apiResponse['wind_variable_direction']
            # metar_wind_gust = apiResponse['wind_gust']
            metar_wind_speed = apiResponse['wind_speed'] # repr, value, spoken
            # metar_wx_codes = apiResponse['wx_codes']
            # metar_wx_raw_str = apiResponse['raw']
            # metar_station = apiResponse['station'] # Just the ICAO code we have already
            metar_time = apiResponse['time'] # repr, dt (datetime)
            # metar_remarks = apiResponse['remarks']
            # metar_remarks_info = apiResponse['remarks_info'] # dewpoint_decimal [repr, value, spoken], temperature_decimal [repr, value, spoken]
            metar_dewpoint = apiResponse['dewpoint'] # repr, value, spoken
            # metar_runway_visibility = apiResponse['runway_visibility']
            metar_temperature = apiResponse['temperature'] # repr, value, spoken
            # metar_units = apiResponse['units'] # altimeter, altitude, temperature, visibility, wind_speed
        except Exception as e:
            print(f'err in setting vars: {e}')

        # End performance timer for total time
        # elapsed_time_in_ms_for_lookup = '{0:.2f}'.format(((time() - start_time) * 1000))
        
        try:
            # Construct embed
            embed = discord.Embed()
            embed.title = f'__**METAR for {airport_icao_code.upper()}**__'
            embed.description = f'**{metar_sanatized_str}**'

            embed.add_field(
                name='__**Airport Information**__',
                value=f'{airport_name} - {airport_city},{airport_state},{airport_country}',
                inline=False
            )

            embed.add_field(
                name='**Station (ICAO/IATA):',
                value=f'{airport_icao_code}/{airport_iata_code}',
                inline=True
            )
            embed.add_field(
                name='**Observed at**:',
                value=metar_time['dt'],
                inline=True
            )
            embed.add_field(
                name='**Dewpoint**:',
                value=f"{metar_dewpoint['value']}°C ({(metar_dewpoint['value'] * (9 / 5)) + 32}°F)",
                inline=True
            )
            embed.add_field(
                name='**Temperature**:',
                value=f"{metar_temperature['value']}°C ({(metar_temperature['value'] * (9 / 5)) + 32}°F)",
                inline=True
            )
            embed.add_field(
                name='**Winds**:',
                value=f"{metar_wind_speed['value']} knots at {metar_wind_dir['value']}°",
                inline=True
            )
            embed.add_field(
                name='**Visibility**:',
                value=f"{metar_visibility['value'] / 1.15078}nm ({metar_visibility['value']}sm)",
                inline=True
            )
            embed.add_field(
                name='**Pressure**:',
                value=f"{'{0:.2f}'.format(metar_altimeter['value'] * 33.86)}hPa ({metar_altimeter['value']} inHg)",
                inline=True
            )

            # embed.add_field(
            #     name='__**Sky Conditions**__:',
            #     value=f"{metar_clouds[0]['']}",
            #     inline=True
            # )

            embed.add_field(
                name='__**Flight Category**__:',
                value=metar_flight_rules,
                inline=True
            )

            embed.add_field(
                name='__**Meta Information**__:',
                value=f"Time at station: {metar_meta['timestamp']}\nStation last updated: {metar_meta['stations_updated']}\nLast cached event: {metar_meta['cache-timestamp']}",
                inline=False
            )

            # Set UTC date on timestamp so discord can parse it
            # embed.timestamp(datetime.utcnow())

            # Send embed
            await ctx.channel.send(embed=embed)

        except Exception as e:
            print(f'Error in main embed: {e}')
