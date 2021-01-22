from redbot.core import Config
from redbot.core import commands

defaults = {"Tasks": []
            }


class Worklist(commands.Cog):
    """
    This will end of being a worklist cog 
    to track you know... tasks
    """

    __author = "blynd"
    __version__ = "1.0.1"

    def __init__(self,bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=88193037185923, force_registration=True)
        self.database.register_guild(**defaults)

    @commands.command()
    async def addtask(self, ctx, task):
        async with self.database.guild(ctx.guild).Tasks() as tasks:
            tasks.append(task.lower())
        await ctx.maybe_send_embed(f"{task.lower()} task was added to worklist.")  



    @commands.command()
    async def tasks(self, ctx):
        data = await self.database.guild(ctx.guild).all()
        await ctx.send(data)