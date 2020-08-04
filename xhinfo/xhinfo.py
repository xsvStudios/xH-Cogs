import discord


from redbot.core import commands

class xsvInfo(commands.Cog):
    """My custom cog"""

    @commands.command(aliases=['ourrules'])
    async def xsvrules(self, ctx):
        """This does stuff!"""
        # Your code will go here
        msg = "This is going to be our rules."
        await ctx.send(msg)