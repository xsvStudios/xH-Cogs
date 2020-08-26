from .xhinfo import Information

# Setup file to read in the cog
def setup(bot):
    bot.add_cog(Information(bot))