from .aviation import Aviation

# Setup file to read in the cog
def setup(bot):
    bot.add_cog(Aviation(bot))