from .volunteer import Volunteer


def setup(bot):
    bot.add_cog(Volunteer(bot))
