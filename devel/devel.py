from redbot.core import commands

class Devel(commands.Cog):
    """
    This is a random development from Blynd.
    
    """

    @commands.command()
    async def testy(self, ctx):
        text = "Hello World"
        await ctx.maybe_embed(simple_text)