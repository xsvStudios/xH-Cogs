from .aviation import Aviation

# Setup file to read in the cog
def setup(bot):
    cog = Aviation(bot)
    bot.add_cog(cog)
    cog.init()