import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box
from typing import Optional


class Information(commands.Cog):
    """
        This is mostly a test cog to try out new things
        before I figure out how to make them work elsewhere
        Generally for commands that don't fit anywhere else or are
        not meant to be used by anyone.
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
    async def ourroles(self, ctx):
        """
            Display rules for xhCommunity
        """
        text = """
__**Community Roles Explained**__

***Members***
```md
> Considered the most important role in the community
# Task
1. Votes on all major community decisions and recruits.
# Removal/Ban
    1. <Moderator(s)> to review case.
    2. Accused <Member> to defend themselves to <Moderator(s)>.
    3. If <Moderator> deems case just. <Moderator> to submit vote to all <Members> for removal/ban. (Majority vote required)
```

__**Support-Teams**__
*Join the team !  Type !apply to join the team.*
*Please read the Community guides.  Commands: !rules !modguide !ourroles !policy*
***Council***
```md
> Senior Members nominated by the community
# Tasks
    1. Manage the operations of the Community to continue the growing success.
    2. Manage <Support-Teams>
    3. Update <Members> on changes.
# Removal/Ban
    1. Any case to be reviewed by <Council>.
```
***Moderator***
```md
# Tasks
    1. Maintain our rules and policies in discord.
# Role Removal
    1. <Council> to review any case against a <Moderator>
```
***Development Team***
```md
# Task
    1. Supports the development and outreach of the Community.
# Role Removal
    1. <Council> to review any case against a <Development-Team>
```
***Game Server Admin***
```md
# Task
    1. Uphold the Community values and policies to not tarnish the group.
# Role Removal
    1. <Council> to review any case against a <Server-Admin>
```

__**Public Roles**__

***Trusted Guest***
```md
> A person deemed trusted to have access to certain channels and voice activation
# Task
    1. Don't be a dick.
# Role Removal
    1. No case required.  <Moderator(s)> decision.
```
***Guests***
```md
# Task
    1. Don't be a dick.
# Kick/Ban
    1. No case required.  <Moderator(s)> decision.
```
***Gameroles***
```md
> Role created for access to hidden game channels.  Join role with !srole  Role has ZERO value
```s
        """
        await ctx.maybe_send_embed(text)

    @commands.command()
    async def modguide(self, ctx):
        text = """**Community Moderator Guide**

```ini
[ General Duties ]
```
**Keep Shit calm**
- Main task.. thats it...

**Mediation** (if required)
- May be requested or required to contain toxicity from spewing.  Case by case basis

```ini
[ Public Channels Practices ]
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

```ini
[ Members Channels Practices ]
```
**Personal Attacks**
- Interject as quickly as possible and stop the discussion
- If the members that were involved went overboard or stepped out of line. Moderator can add a warning for future review on the instance a member ever gets put in for a member removal vote."""
        await ctx.maybe_send_embed(text)


        
    @commands.command()
    async def joinus(self, ctx):
        text = """*
        **Join our Community**
Interested in joining the community?  We have implemented a sponsorship program for new recruits.  Have no fear, the process is simple..

**Step One -  Application Process**
Application Requirements

2. Require 2 sponsors that must be community members. 

*Need a sponser?  Type `!apply` in any channel.  Fill out the form and lets see who is willing.*

**Step Two - Junior Member Status**
After your application for Junior Tags is approved.  You will have a **6** month trial period where we judge you as a person.  During this time there are a few things that can remove your **Junior Member** status.

Requirements
1. Don't be a Dick. 
2. Maintain two sponsors at all times.
3. Maintain less the 3 warnings for duration of sponsorship.


**Step Three - Its VOTING time**
After your **6** month period your application for **Member** tags will go to a community vote.  Vote will last **7** days.  **Majority** vote required.

        """
        await ctx.maybe_send_embed(text)


    @commands.command()
    async def donate(self, ctx: commands.Context):
        """
            Become a Community Donor for perks!
            https://xsvcommunity.com/donate
        """
        msg = (
            "Help support the Communities growth."
            "Donor's get a longlist of perks ranging from Streaming services, "
            "VPN access, 0365, 1TB Cloud space, and more :smile:"
        )
        await ctx.send(msg)