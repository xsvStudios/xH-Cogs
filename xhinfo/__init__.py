from .xhinfo import xhInfo

# Setup file to read in the cog
def setup(bot):
    bot.add_cog(xhInfo(bot))