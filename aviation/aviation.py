import discord
from redbot.core import commands, checks, Config

import datetime
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

    def pickRecentUNIXTimestamp(self):
        try:
            response = requests.get('https://api.rainviewer.com/public/maps.json')
            blah = response.json()
            return blah[len(blah) - 1]
        except:
            return None

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

        try:
            # Do the api call
            response = requests.get(apiurl, headers={ 'Authorization': f'Bearer {apikey}' })

            # Make sure it went well...
            if response.status_code != 200:
                # TODO: REMOVE WHEN IT WORKS
                return None

            return response.json()

        except Exception as e:
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
            airport_latitude = station_obj['lat']
            airport_longitude = station_obj['lon']
            # airport_timezone = station_obj['tz']

            # End performance timer for lookup
           #  elapsed_time_in_ms_for_lookup = '{0:.2f}'.format(((time() - start_time) * 1000))

            """
                Perform API call to actually get metar weather information.
            """
            apiResponse = self.getMetarInfo(airport_icao_code.upper(), apikey)
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
        except:
            return await ctx.send('It seems something went wrong when setting some variables. Please try another one later...')

        # End performance timer for total time
        # elapsed_time_in_ms_for_lookup = '{0:.2f}'.format(((time() - start_time) * 1000))

        try:
            # Construct the body for the embed so it looks all nice
            body =  f"**{metar_sanatized_str}**\n\n"
            body += f"**Airport Information**: {airport_name} - {airport_city}, {airport_state}, {airport_country} [long/lat][**{airport_longitude}**/**{airport_latitude}**]\n\n"

            # Construct if the station has an IATA code or not
            if airport_iata_code == '' or airport_iata_code == None:
                body += f"**Station (ICAO)**: {airport_icao_code}\n"
            else:
                body += f"**Station (ICAO/IATA)**: {airport_icao_code}/{airport_iata_code}\n"

            # Do some string magic to make the datetime what these guys want...
            t = metar_time['dt'].replace(':', '')
            body += f"**Observed at**: {t[: t.find('T')]} {t[t.find('T') + 1 : t.find('Z') - 2]}Z\n"
            body += f"**Temperature**: {metar_temperature['value']}°C ({'{0:.2f}'.format((metar_temperature['value'] * (9 / 5)) + 32)}°F)\n"
            body += f"**Dewpoint**: {metar_dewpoint['value']}°C ({'{0:.2f}'.format((metar_dewpoint['value'] * (9 / 5)) + 32)}°F)\n"
            body += f"**Winds**: {metar_wind_dir['value']}° at {metar_wind_speed['value']} knots\n"
            body += f"**Visibility**: {metar_visibility['value']}sm\n"
            body += f"**Pressure**: {'{0:.2f}'.format(metar_altimeter['value'] * 33.86)}hPa ({metar_altimeter['value']} inHg)\n\n"

            # Same as above
            ts = metar_meta['timestamp'].replace(':', '')
            body += f"**Time at station**: {ts[: ts.find('T')]} {ts[ts.find('T') + 1 : ts.find('Z') - 2]}Z\n"
            body += f"**Station last updated**: {metar_meta['stations_updated']}\n"

            # Construct embed
            embed = discord.Embed(
                title=f'__**METAR for {airport_icao_code.upper()}**__',
                description=body,
                color=0xd90be0,
            )

            # TODO: do some clouds data
            # if len(metar_clouds) > 0:
            #     embed.add_field(
            #         name='__**Sky Conditions**__:',
            #         value=f"{metar_clouds}",
            #         inline=False
            #     )

            # VFR, IFR, etc...
            embed.add_field(
                name='__**Flight Category**__:',
                value=f'**{metar_flight_rules}**',
                inline=False
            )

            # Set UTC date on timestamp so discord can parse it
            embed.timestamp = datetime.datetime.utcnow()

            # Set author stuff
            embed.set_author(
                name=ctx.message.author,
                icon_url=ctx.message.author.avatar_url
            )

            # Experimental stuff
            # https://www.rainviewer.com/api.html
            # unixTime = self.pickRecentUNIXTimestamp()
            # if unixTime != None:
            #     embed.set_image(
            #         url=f"https://tilecache.rainviewer.com/v2/radar/{unixTime}/512/2/{airport_latitude}/{airport_longitude}/1/0_0.png"
            #     )

            # Send embed
            return await ctx.send(embed=embed)

        except:
            return await ctx.send('It seems something went really wrong building the embed. Please try again later...')
