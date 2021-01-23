import asyncio
import discord

from redbot.core import Config
from redbot.core import commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
  

defaults = {
    "id": 0,
    "description": "fuck you",
    "priority": -1,
    "assigned": "nobody"
    "due_date": 1
}


defaults = {
  "Tasks": {
    "task_id":{
      "id": 0,
      "description": "",
      "priority": 0,
      "assigned": "",
      "due_date": ""
    }
  }
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
        lastid = [x for x in defaults if x['id']]

        async with self.database.guild(ctx.guild).Tasks() as tasks:
            tasks.append(task)

        
        await ctx.maybe_send_embed(f"{task} task was added to worklist.")  



    @commands.command()
    async def tasks(self, ctx):
        """
        Prints all tasks on worklist
        """
        data = await self.database.guild(ctx.guild).all()
        await ctx.maybe_send_embed(data)




    # @commands.command()
    # async def newtask(self, ctx: commands.Context, *, format_msg: str) -> None:)
    # """

    # """

    # guild = ctx.message.guild
    # guild_settings = await self.config.guild(guild).description()
    # guild_settings.append(format_msg)
    # await self.config.guild(guild).description.set(guild_settings)
    # await ctx.send(_("This should be added"))