from redbot.core import commands

class Devel(commands.Cog):
    """Testing over"""

    @commands.command()
    async def testy(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can break things thats for sure!")