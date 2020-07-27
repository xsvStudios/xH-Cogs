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
        """
            * metar <station_id>

            Takes the input station id and outputs information that is associated with it with the most updated online info avaliable.

            Example: <prefix>METAR KORD
                <param> is station id. All station ID's found here:
                    https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
        """

        try:
            return await ctx.send('This is a test message to make sure the cog is working properly.')
        except Exception as e:
            return await ctx.send(f'Fatal exception in metar command: {e}')
