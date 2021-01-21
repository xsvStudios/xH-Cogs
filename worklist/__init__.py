from .worklist import Worklist


def setup(bot):
    bot.add_cog(Worklist())