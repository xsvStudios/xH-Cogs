import discord

from redbot.core import Config, commands
  

defaults = {
    "Worklist": []
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
    async def addtask(self, ctx: commands.Context, *, format_msg: str):
        """
        Add a task to worklist
        """
        task = {
            "id": -1,
            "description": "",
            }

        async with self.database.guild(ctx.guild).Worklist() as tasks:
            taskid = len(tasks) + 1 if len(tasks) > 0 else 1
            task['id'] = taskid
            task['description'] = format_msg
            tasks.append(task)

        
        await ctx.maybe_send_embed(f"{task['description']} task was added to worklist.")  



    @commands.command()
    async def tasks(self, ctx):
        """
        Prints all tasks on worklist
        """
        data = await self.database.guild(ctx.guild).Worklist()
        await ctx.maybe_send_embed(str(data))


    @commands.command()
    async def taskswhat(self, ctx: commands.Context) -> None:
        """

        """
        guild =  ctx.message.guild
        worklists_test = await self.config.guild(guild).description()
        for m in worklists_test:
            msg += "  {}. {}\n".format(c)
        for page in pagify(msg, ["\n", " "], shorten_by=20):
            await ctx.send("```\n{}\n```".format(page))