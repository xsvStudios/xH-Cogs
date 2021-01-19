from redbot.core import commands

class Devel(commands.Cog):
    """
    This is a random development from Blynd.
    
    """
      def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def testy(self, ctx):
        text = "Hello World"
        await ctx.maybe_embed(simple_text)