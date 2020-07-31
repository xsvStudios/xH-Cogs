from .info import xhInfo


def setup(bot):
    n = xhInfo(bot)
    bot.add_cog(n)