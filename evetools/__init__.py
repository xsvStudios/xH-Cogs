from .evetools import EveTools

# Setup file to read in the cog
def setup(bot):
    bot.add_cog(EveTools(bot))