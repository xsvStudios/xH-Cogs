import discord
from redbot.core import commands

class Aviation(commands.Cog):
    """
        Has some simple aviation commands such as checking for airport weather, tracking planes, etc...
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def metar(self, ctx, station_id: str):
        """
            Gets the current weather information from a specified airport IATA or ICAO airport code.

            General list of airports with IATA and ICAO codes: https://en.wikipedia.org/wiki/Lists_of_airports
            IATA Codes (3 letters): https://en.wikipedia.org/wiki/IATA_airport_code
            ICAO Codes (4 letters): https://en.wikipedia.org/wiki/ICAO_airport_code
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

        try:
            return await ctx.send('This is a test message to make sure the cog is working properly.')
        except Exception as e:
            return await ctx.send(f'Fatal exception in metar command: {e}')
