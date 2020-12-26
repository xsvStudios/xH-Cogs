from .aviation import Aviation

# Setup file to read in the cog
desf setup(bot):
    bot.add_cog(Aviation(bot))