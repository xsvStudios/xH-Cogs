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


    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"


    @commands.command()
    async def addtask(self, ctx: commands.Context, *, task: str):
        """
        Add a task to worklist
        """
        async with self.database.guild(ctx.guild).Tasks() as tasks:
            tasks.append(task)
        await ctx.maybe_send_embed(f"{task} task was added to worklist.")  



    @commands.command()
    async def tasks(self, ctx):
        """
        Prints all tasks on worklist
        """
        data = await self.database.guild(ctx.guild).all()
        await ctx.send(data)