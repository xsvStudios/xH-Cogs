from redbot.core import Config
from redbot.core import commands

defaults = {"Tasks": []
            }


class Worklist: 

    def __init__(self):
        self.database = Config.get_conf(self, identifier=88193037185923, force_registration=True)
        self.database.register_guild(**defaults)

    @commands.command()
    async def addtask(self, ctx, task: str):
        async with self.database.guild(ctx.guild).Tasks() as tasks:
            tasks.append(task.lower())
        await ctx.maybe_send_embed(f"{task.lower()} task was added to worklist.")  