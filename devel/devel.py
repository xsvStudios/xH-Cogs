from redbot.core import commands

class Devel(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def testy(self, ctx):
        """This does stuff!"""
        # Messing with embeds for a bit.
        text = "This is a embed test?  please work?"
        await ctx.maybe_send_embed(text)