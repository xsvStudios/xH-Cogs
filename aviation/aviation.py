import discord
from redbot.core import commands

class Aviation(commands.Cog):
    """
        Author: AWildTeddyBear (Sgt.Cuddles#0001)

        Has some simple commands in here for avaiation nerds for a discord bot.

        Cog requested by: jbaros#4250
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def metar(self, ctx, station_id: str):
        f"""
            Gets the current weather information from a specified airport IATA or ICAO airport code.
            
            General list of airports with IATA and ICAO codes: https://en.wikipedia.org/wiki/Lists_of_airports
            IATA Codes (3 letters): https://en.wikipedia.org/wiki/IATA_airport_code
            ICAO Codes (4 letters): https://en.wikipedia.org/wiki/ICAO_airport_code

            Will return the data in an embed to the user with useful weather information of the airport.

            **Example**:
            {ctx.prefix}metar **kord**
            {ctx.prefix}metar **aaa**
        """

        try:
            return await ctx.send('This is a test message to make sure the cog is working properly.')
        except Exception as e:
            return await ctx.send(f'Fatal exception in metar command: {e}')
