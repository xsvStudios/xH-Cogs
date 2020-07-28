import discord
from redbot.core import commands

from datetime import datetime
import json

class Aviation(commands.Cog):
    """
        Has some simple aviation commands such as checking for airport weather, tracking planes, etc...
    """

    def __init__(self, bot):
        self.bot = bot

    def airportLookup(self, airport_code: str, airport_code_type: str):
        """
            Loads the airport lookup table from airports.json and loads it into memory.
            Searches the lookup file for the specefied ICAO or IATA code and returns the hit if found.
            TODO: Make this more efficient by loading it only once in the __init__ of the cog so we don't waste time loading it again.
        """

        try:
            # Open local JSON file
            with open('airports.json', 'r', encoding='utf-8') as f:
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

    def getMetarInfo(self):
        """
            TODO: Add description here
        """
        # TODO: Add datagrabbing here for the actual metar data. Also include performance metric in returned object.

        return NotImplemented

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
            return await ctx.send(f'Your input must be an ICAO or IATA code. Get more info by typing: {ctx.prefix}help {ctx.command}')

        # TODO: Do lookup table here and get information on it such as airport name, etc...

        # TODO: Get data here and store it in an dictionary and perform datachecks on it

        """
            Get data from respective code type.
        """

        # Define global object to assign in the case types below
        station_obj = None

        if len(station_id) == 4:
            # ICAO Code handling

            # Lookup ICAO code and return object if found
            icao_lookup = self.airportLookup(station_id, 'ICAO')
            print(icao_lookup)
            if icao_lookup == None:
                return await ctx.send(f'Error: The airport ICAO code with input ID \'{station_id}\' was not found!')

            # Lookup was successful
            station_obj = icao_lookup
        elif len(station_id) == 3:
            # IATA Code handling

            # Lookup IATA code and return object if found
            iata_lookup = self.airportLookup(station_id, 'IATA')
            print(iata_lookup)
            if iata_lookup == None:
                return await ctx.send(f'Error: The airport IATA code with input ID \'{station_id}\' was not found!')

            # Lookup was successful
            station_obj = iata_lookup
        else:
            # If this gets hit, then it somehow avoided the filters? How???
            return await ctx.send(f'Your input must be an ICAO or IATA code. Get more info by typing: {ctx.prefix}help {ctx.command}')

        # Exit if something bad happened. (over-engineering, but whatever)
        if station_obj is None:
            return await ctx.send('An error occured looking up your airport code. Please try again or try a different code.')

        # temp
        return await ctx.send(station_obj)

        # Construct embed
        try:
            embed = discord.Embed(
                title=f'',
                description='',
                color=0x8b0eeb,
            )

            # Set UTC date on timestamp so discord can parse it
            embed.timestamp(datetime.utcnow())

            # Send embed
            return await ctx.send(embed=embed)

        except:
            return None
