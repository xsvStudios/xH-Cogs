import discord
import time
import asyncio
import logging
from typing import Optional

from redbot.core import Config, commands, checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.i18n import Translator, cog_i18n


@cog_i18n(_)
class EveTools(BaseCog):
    """
    Eve Tools
    """
    __author__ = ["Blynd"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=11_23_0788, force_registration=True)
        self.config.register_global(timeout=5)
        self.timeout = None

        
    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
            Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def edit_process_commands(self, message: discord.Message):
        """Same as Red's method (Red.process_commands), but dont dispatch message_without_command.  Thanks Zeph."""
        if not message.author.bot:
            ctx = await self.bot.get_context(message)
            await self.bot.invoke(ctx)

# Peplaces the base ping command of Red.

    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def ping(self, ctx):
        """Reply with latency of bot"""
        latency = self.bot.latency * 1000
        emb = discord.Embed(title="Pong ! \N{TABLE TENNIS PADDLE AND BALL} ", color=discord.Color.red())
        emb.add_field(
            name="API:", value=chat.box(str(round(latency)) + " ms"),
        )
        emb.add_field(name="Message:", value=chat.box("…"))
        emb.add_field(name="Typing:", value=chat.box("…"))

        before = time.monotonic()
        message = await ctx.send(embed=emb)
        ping = (time.monotonic() - before) * 1000
        # Thanks preda, but i copied this from MAX's version, and fixator have made it even better.
        if len(self.bot.latencies) > 1:
            # The chances of this in near future is almost 0, but who knows, what future will bring to us?
            shards = [
                f"Shard {shard + 1}/{self.bot.shard_count}: {round(pingt * 1000)}ms"
                for shard, pingt in self.bot.latencies
            ]
            emb.add_field(name="Shards:", value=chat.box("\n".join(shards)))
        emb.colour = await ctx.embed_color()
        emb.set_field_at(
            1,
            name="Message:",
            value=chat.box(
                str(int((message.created_at - ctx.message.created_at).total_seconds() * 1000))
                + " ms"
            ),
        )
        emb.set_field_at(2, name="Typing:", value=chat.box(str(round(ping)) + " ms"))

        await message.edit(embed=emb)


# Command Editor.
# This adds a listener to bot to look for message edit if a command is mistyped.
    @commands.command()
    @checks.is_owner()
    async def edittime(self, ctx, *, timeout: float):
        """
        Change how long the bot will listen for message edits to invoke as commands.
        Defaults to 5 seconds.
        Set to 0 to disable.
        """
        if timeout < 0:
            timeout = 0
        await self.config.timeout.set(timeout)
        self.timeout = timeout
        await ctx.tick()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.edited_at:
            return
        if before.content == after.content:
            return
        if self.timeout is None:
            self.timeout = await self.config.timeout()
        if (after.edited_at - after.created_at).total_seconds() > self.timeout:
            return
        await self.edit_process_commands(after)



    @commands.command(hidden=True)
    async def say(self, ctx: commands.Context, *, msg: str):
        """Say things as the bot"""
        await ctx.send(msg)