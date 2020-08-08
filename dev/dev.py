import asyncio
import inspect
import io
import subprocess
import textwrap
import traceback
from subprocess import Popen
import re
import threading
from asyncio.subprocess import PIPE, STDOUT
from contextlib import redirect_stdout
import inspect

import discord
from discord import Message, message
from redbot.core import checks, commands
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, pagify, bold, inline
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.cogs.downloader.converters import InstalledCog
from redbot.cogs.downloader import Downloader

"""
Notice:

95% of the below code came from R.Danny which can be found here:

https://github.com/Rapptz/RoboDanny/blob/master/cogs/repl.py
"""

_ = Translator("Dev", __file__)

START_CODE_BLOCK_RE = re.compile(r"^((```py)(?=\s)|(```))")

BaseCog = getattr(commands, "Cog", object)

class xsvDev(BaseCog):
    """Various development focused utilities."""

    __version__ = "3.2.3"
    __author__ = [
        "R.Danny",
        "Toby",
        "Will",
        "Blynd",
        "Michael",
        "Eslyium",
        "Preda",
        "NeuroAssassin",
        "TrustyJAID",
    ]

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
            Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return START_CODE_BLOCK_RE.sub("", content)[:-3]

        # remove `foo`
        return content.strip("` \n")

    @staticmethod
    def get_syntax_error(e):
        """Format a syntax error to send to the user.

        Returns a string representation of the error formatted as a codeblock.
        """
        if e.text is None:
            return box("{0.__class__.__name__}: {0}".format(e), lang="py")
        return box("{0.text}{1:>{0.offset}}\n{2}: {0}".format(e, "^", type(e).__name__), lang="py")

    @staticmethod
    def get_pages(msg: str):
        """Pagify the given message for output to the user."""
        return pagify(msg, delims=["\n", " "], priority=True, shorten_by=10)

    @staticmethod
    def sanitize_output(ctx: commands.Context, input_: str) -> str:
        """Hides the bot's token from a string."""
        token = ctx.bot.http.token
        return re.sub(re.escape(token), "[EXPUNGED]", input_, re.I)

    @commands.command()
    @checks.is_owner()
    async def debug(self, ctx, *, code):
        """Evaluate a statement of python code.

        The bot will always respond with the return value of the code.
        If the return value of the code is a coroutine, it will be awaited,
        and the result of that will be the bot's response.

        Note: Only one statement may be evaluated. Using await, yield or
        similar restricted keywords will result in a syntax error. For multiple
        lines or asynchronous code, see [p]repl or [p]eval.

        Environment Variables:
            ctx      - command invokation context
            bot      - bot object
            channel  - the current channel object
            author   - command author's member object
            message  - the command's message object
            discord  - discord.py library
            commands - redbot.core.commands
            _        - The result of the last dev command.
        """
        env = {
            "bot": ctx.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "discord": discord,
            "commands": commands,
            "_": self._last_result,
        }

        code = self.cleanup_code(code)

        try:
            result = eval(code, env)
        except SyntaxError as e:
            await ctx.send(self.get_syntax_error(e))
            return
        except Exception as e:
            await ctx.send(box("{}: {!s}".format(type(e).__name__, e), lang="py"))
            return

        if inspect.isawaitable(result):
            result = await result

        self._last_result = result
        result = self.sanitize_output(ctx, str(result))

        await ctx.send_interactive(self.get_pages(result), box_lang="py")

    @commands.command(name="eval")
    @checks.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Execute asynchronous code.

        This command wraps code into the body of an async function and then
        calls and awaits it. The bot will respond with anything printed to
        stdout, as well as the return value of the function.

        The code can be within a codeblock, inline code or neither, as long
        as they are not mixed and they are formatted correctly.

        Environment Variables:
            ctx      - command invokation context
            bot      - bot object
            channel  - the current channel object
            author   - command author's member object
            message  - the command's message object
            discord  - discord.py library
            commands - redbot.core.commands
            _        - The result of the last dev command.
        """
        env = {
            "bot": ctx.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "discord": discord,
            "commands": commands,
            "_": self._last_result,
        }

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = "async def func():\n%s" % textwrap.indent(body, "  ")

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env["func"]
        result = None
        try:
            with redirect_stdout(stdout):
                result = await func()
        except:
            printed = "{}{}".format(stdout.getvalue(), traceback.format_exc())
        else:
            printed = stdout.getvalue()
            await ctx.tick()

        if result is not None:
            self._last_result = result
            msg = "{}{}".format(printed, result)
        else:
            msg = printed
        msg = self.sanitize_output(ctx, msg)

        await ctx.send_interactive(self.get_pages(msg), box_lang="py")

    @commands.command()
    @checks.is_owner()
    async def repl(self, ctx):
        """Open an interactive REPL.

        The REPL will only recognise code as messages which start with a
        backtick. This includes codeblocks, and as such multiple lines can be
        evaluated.

        You may not await any code in this REPL unless you define it inside an
        async function.
        """
        variables = {
            "ctx": ctx,
            "bot": ctx.bot,
            "message": ctx.message,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "author": ctx.author,
            "_": None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send(
                _("Already running a REPL session in this channel. Exit it with `quit`.")
            )
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send(_("Enter code to execute or evaluate. `exit()` or `quit` to exit."))

        while True:
            response = await ctx.bot.wait_for("message", check=MessagePredicate.regex(r"^`", ctx))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ("quit", "exit", "exit()"):
                await ctx.send(_("Exiting."))
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count("\n") == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, "<repl session>", "eval")
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, "<repl session>", "exec")
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables["message"] = response

            stdout = io.StringIO()

            msg = ""

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except:
                value = stdout.getvalue()
                msg = "{}{}".format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    msg = "{}{}".format(value, result)
                    variables["_"] = result
                elif value:
                    msg = "{}".format(value)

            msg = self.sanitize_output(ctx, msg)

            try:
                await ctx.send_interactive(self.get_pages(msg), box_lang="py")
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(_("Unexpected error: `{}`").format(e))

    @commands.command()
    @checks.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        """Mock another user invoking a command.

        The prefix must not be entered.
        """
        msg = copy(ctx.message)
        msg.author = user
        msg.content = ctx.prefix + command

        ctx.bot.dispatch("message", msg)

    @commands.command(name="mockmsg")
    @checks.is_owner()
    async def mock_msg(self, ctx, user: discord.Member, *, content: str):
        """Dispatch a message event as if it were sent by a different user.

        Only reads the raw content of the message. Attachments, embeds etc. are
        ignored.
        """
        old_author = ctx.author
        old_content = ctx.message.content
        ctx.message.author = user
        ctx.message.content = content

        ctx.bot.dispatch("message", ctx.message)

        # If we change the author and content back too quickly,
        # the bot won't process the mocked message in time.
        await asyncio.sleep(2)
        ctx.message.author = old_author
        ctx.message.content = old_content



    @commands.command(aliases=["shell"])
    @checks.is_owner()
    async def bash(self, ctx, *, arg):
        """Bash shell"""
        proc = await asyncio.create_subprocess_shell(arg, stdin=None, stderr=STDOUT, stdout=PIPE)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        await ctx.send(f"```ini\n\n[Bash Input]: {arg}\n```")
        await ctx.send_interactive(msg, box_lang="py")



    @commands.command()
    @checks.is_owner()
    async def getsource(self, ctx, *, cmd: str):
        """
        Get the source code of a command
        Credits to Nesroht
        """
        cmd = self.bot.get_command(cmd)
        if cmd is None:
            await ctx.send("> That command doesn't seem to exist.")
            return
        source_code = inspect.getsource(cmd.callback)
        tmpp = []
        p = []
        for page in pagify(source_code, escape_mass_mentions=True, page_length=1900):
            tmpp.append("```py\n" + str(page).replace("```", "``") + "```")
        maxi = len(tmpp)
        i = 1
        for page in tmpp:
            p.append(f"Page {i}/{maxi}\n" + page)
            i += 1
        await menu(ctx, p, controls=DEFAULT_CONTROLS)


    @commands.command()
    @commands.is_owner()
    async def update(self, ctx: commands.Context):
        """Updates installed cogs and reloads the loaded ones automatically."""
        ctx.assume_yes = True
        cog_upd_command = ctx.bot.get_command("cog update")
        if cog_upd_command is None:
            await ctx.send("Welp, that ain't gonna happen. \nYou need to `{}load downloader` first.".format(ctx.prefix))
        else:
            await ctx.invoke(cog_upd_command)