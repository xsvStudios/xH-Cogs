from .devel import Devel

async def setup(bot):
    cog = Devel(bot)
    bot.add_cog(cog)
    await cog.initalize()