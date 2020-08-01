import discord
import time
import asyncio
import logging

from typing import Optional
from laggron_utils.logging import close_logger, DisabledConsoleOutput

from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.tunnel import Tunnel

log = logging.getLogger("red.xsv-cogs.evetools")
_ = Translator("Say", __file__)
BaseCog = getattr(commands, "Cog", object)

# Red 3.0 backwards compatibility, thanks Sinbad
listener = getattr(commands.Cog, "listener", None)
if listener is None:

    def listener(name=None):
        return lambda x: x

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



# Say.  Brought to life by "El Laggron".  Sincerely appreciate the ease of use you created here.
    async def say(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel], text: str, files: list
    ):
        if not channel:
            channel = ctx.channel
        if not text and not files:
            await ctx.send_help()
            return

        # preparing context info in case of an error
        if files != []:
            error_message = (
                "Has files: yes\n"
                f"Number of files: {len(files)}\n"
                f"Files URL: " + ", ".join([x.url for x in ctx.message.attachments])
            )
        else:
            error_message = "Has files: no"

        # sending the message
        try:
            await channel.send(text, files=files)
        except discord.errors.HTTPException as e:
            if not ctx.guild.me.permissions_in(channel).send_messages:
                author = ctx.author
                try:
                    await ctx.send(
                        _("I am not allowed to send messages in ") + channel.mention,
                        delete_after=2,
                    )
                except discord.errors.Forbidden:
                    await author.send(
                        _("I am not allowed to send messages in ") + channel.mention,
                        delete_after=15,
                    )
                    # If this fails then fuck the command author
            elif not ctx.guild.me.permissions_in(channel).attach_files:
                try:
                    await ctx.send(
                        _("I am not allowed to upload files in ") + channel.mention, delete_after=2
                    )
                except discord.errors.Forbidden:
                    await author.send(
                        _("I am not allowed to upload files in ") + channel.mention,
                        delete_after=15,
                    )
            else:
                log.error(
                    f"Unknown permissions error when sending a message.\n{error_message}",
                    exc_info=e,
                )

    @commands.command(name="say")
    @checks.guildowner()
    async def _say(self, ctx, channel: Optional[discord.TextChannel], *, text: str = ""):
        """
        Make the bot say what you want in the desired channel.
        If no channel is specified, the message will be send in the current channel.
        You can attach some files to upload them to Discord.
        Example usage :
        - `!say #general hello there`
        - `!say owo I have a file` (a file is attached to the command message)
        """

        files = await Tunnel.files_from_attatch(ctx.message)
        await self.say(ctx, channel, text, files)

    @commands.command(name="sayd", aliases=["sd"])
    @checks.guildowner()
    async def _saydelete(self, ctx, channel: Optional[discord.TextChannel], *, text: str = ""):
        """
        Same as say command, except it deletes your message.
        If the message wasn't removed, then I don't have enough permissions.
        """

        # download the files BEFORE deleting the message
        author = ctx.author
        files = await Tunnel.files_from_attatch(ctx.message)

        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            try:
                await ctx.send(_("Not enough permissions to delete messages."), delete_after=2)
            except discord.errors.Forbidden:
                await author.send(_("Not enough permissions to delete messages."), delete_after=15)

        await self.say(ctx, channel, text, files)

    @commands.command(name="interact")
    @checks.guildowner()
    async def _interact(self, ctx, channel: discord.TextChannel = None):
        """Start receiving and sending messages as the bot through DM"""

        u = ctx.author
        if channel is None:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(
                    _(
                        "You need to give a channel to enable this in DM. You can "
                        "give the channel ID too."
                    )
                )
                return
            else:
                channel = ctx.channel

        if u in self.interaction:
            await ctx.send(_("A session is already running."))
            return

        message = await u.send(
            _(
                "I will start sending you messages from {0}.\n"
                "Just send me any message and I will send it in that channel.\n"
                "React with ❌ on this message to end the session.\n"
                "If no message was send or received in the last 5 minutes, "
                "the request will time out and stop."
            ).format(channel.mention)
        )
        await message.add_reaction("❌")
        self.interaction.append(u)

        while True:

            if u not in self.interaction:
                return

            try:
                message = await self.bot.wait_for("message", timeout=300)
            except asyncio.TimeoutError:
                await u.send(_("Request timed out. Session closed"))
                self.interaction.remove(u)
                return

            if message.author == u and isinstance(message.channel, discord.DMChannel):
                files = await Tunnel.files_from_attatch(message)
                if message.content.startswith(tuple(await self.bot.get_valid_prefixes())):
                    return
                await channel.send(message.content, files=files)
            elif (
                message.channel != channel
                or message.author == channel.guild.me
                or message.author == u
            ):
                pass

            else:
                embed = discord.Embed()
                embed.set_author(
                    name="{} | {}".format(str(message.author), message.author.id),
                    icon_url=message.author.avatar_url,
                )
                embed.set_footer(text=message.created_at.strftime("%d %b %Y %H:%M"))
                embed.description = message.content
                embed.colour = message.author.color

                if message.attachments != []:
                    embed.set_image(url=message.attachments[0].url)

                await u.send(embed=embed)

    @listener()
    async def on_reaction_add(self, reaction, user):
        if user in self.interaction:
            channel = reaction.message.channel
            if isinstance(channel, discord.DMChannel):
                await self.stop_interaction(user)

    @listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandInvokeError):
            return
        if not ctx.command.cog_name == self.__class__.__name__:
            # That error doesn't belong to the cog
            return
        with DisabledConsoleOutput(log):
            log.error(
                f"Exception in command '{ctx.command.qualified_name}'.\n\n",
                exc_info=error.original,
            )

    async def stop_interaction(self, user):
        self.interaction.remove(user)
        await user.send(_("Session closed"))

    def __unload(self):
        self.cog_unload()

    def cog_unload(self):
        log.debug("Unloading cog...")
        for user in self.interaction:
            self.bot.loop.create_task(self.stop_interaction(user))
        close_logger(log)