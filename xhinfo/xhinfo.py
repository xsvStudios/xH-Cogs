import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box
from typing import Optional


class Information(commands.Cog):
    """
        This is mostly a test cog to try out new things
        before I figure out how to make them work elsewhere
        Generally for commands that don't fit anywhere else or are
        not meant to be used by anyone except TrustyBot
    """
    __author__ = ["Blynd"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
            Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    @commands.command()
    async def ourrules(self, ctx):
        """
            Display rules for xhCommunity
        """
        msg = """**Moderator Guide**

```css
< General >
**Keep Shit calm**
- Main task.. thats it...
**Mediation** (if required)
- May be requested or required to contain toxicity from spewing.  Case by case basis

```css
< Public Channels >
```
**Personal Attacks**
- Moderator to interject and drop the gavel on the discussion.
- Personal attack posts to be removed.
- If required the entire conversation to be removed.

**Political Based Posts** *(within means)*
- Keep it in the Politics Channels
- Remove any posts that are outside of the channel.
- Personal attacks removed.

**Disputes**
- Interject the situation and STOP it.
- If Members tell them, move it to members channel or private.
- If not-members tell, then stfu nicely and move to private.
- Remove posts is deemed necessary.

**NSFW**
- Remove posts from public channels that may be classified as NSFW. *Moderator discretion*

```css
< Members Channels >
```
**Personal Attacks**
- Interject as quickly as possible and stop the discussion
- If the members that were involved went overboard or stepped out of line. Moderator can add a warning for future review on the instance a member ever gets put in for a member removal vote."""
        await ctx.send(msg)

    @commands.command()
    async def test(self, ctx):
        text = "Hello World"
        await ctx.maybe_send_embed(simple_text)

    @commands.command()
    async def donate(self, ctx: commands.Context):
        """
            Donate to the development of TrustyBot!
            https://trustyjaid.com
        """
        msg = (
            "Help support me and my work on TrustyBot "
            "by buying my album or donating, details "
            "on my website at the bottom :smile: https://trustyjaid.com/"
        )
        await ctx.send(msg)