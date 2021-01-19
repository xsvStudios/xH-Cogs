from .devel import Devel

# Setup file to read in the cog
def setup(bot):
    bot.add_cog(Devel(bot))