from .dev import xsvDev


def setup(bot):
    bot.add_cog(xsvDev(bot))
