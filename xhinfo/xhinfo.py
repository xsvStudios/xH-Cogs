import discord
import random
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box
from typing import Optional


class Information(commands.Cog):
    """
        Community Information and Guides
    """
    __author__ = ["Blynd"]
    __version__ = "1.2.6"

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
            xH Community Roles Explained
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
        """
        xH Moderator Guidelines and Policies
        """
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
        """
        Join our team!
        """
        text = """
**Join this Community**
Interested in joining the community?  We have implemented a sponsorship program for new recruits.  Have no fear, the process is simple..

**Step One -  Application Process**
__Application Requirements__
1: You need 2 sponsors that must be community members. 
*Need a sponser?  Type `!apply` in any channel.  Fill out the form and lets see who is willing.*

**Step Two - Junior Member Status**
After your application for Junior Tags is approved.  You will have a **6** month trial period where we judge you as a person.  During this time there are a few things that can remove your **Junior Member** status.

__Requirements__
1: Don't be a Dick. 
2: Maintain two sponsors at all times.
3: Maintain less the 3 warnings for duration of sponsorship.

__Sponsorship__
Your sponsor is responsble for you and we will hold them accountable for your BS.  At any time you could lose a sponser.  Few things happen if someone pulls out...
1: Loss of Sponsor
    - If you lose **1** sponser, you must find a replacement sponsor with 72 hours. Your sponsorship period restarts.
    - If you lose **2** sponsers, your **Junior** role will be removed and you trial is over.  Goodbye.
3: 1 warning will be added to your account.

**Step Three - Its VOTING time**
After your **6** month period your application for **Member** tags will go to a community vote.  Vote will last **7** days.  **Majority** vote required.
        """
        await ctx.maybe_send_embed(text)


#     @commands.command()
#     async def rules(self, ctx):
#         """
#         Our community Rules
#         """
#         text = """
# **Community Rules**
# *We give the benefit of the doubt...  Don't be a dumbass and you'll be fine.*

# __**Don't be a dick..**__
# People can be dumb, we know this. We will deal with the problem swiftly. Do not antagonize.
# __**Act like an adult…**__
# You are NOT more important than your neighbor…  Community is 18+
# __**Racism is ZERO TOLERANCE**__
# Period.  You want your opinion, cool.. Keep it to PM’s and out of public discord.
# __**Harassment is ZERO TOLERANCE**__
# There is a difference between talking shit as friends and attacking someone… you should know it. If you don’t, we will help make it clear.
# __**Excessive Bashing is ZERO TOLERANCE**__
# Whether it's our group, or another community - don't bash them or their staff. Not cool and we do not support it.
# __**Trolling**__
# If you're making off-topic comments, taking threads off-topic, or posting random irrelevant material, you're likely to find a boot in your ass.
# __**NSFW Material**__
# Not allowed in public areas of discord, sorry. 
# We do have a members only NSFW channel.  This is NOT public by design.  
# __**Community Promotions**__
# The community has approved partner communities. If they are not on the approved list don't share it. Partner list will be available with command !partners very soon.
#         """
#         await ctx.maybe_send_embed(text)

    @commands.command()
    async def donate(self, ctx: commands.Context):
        """
            Donate to help support our community!
        """
        msg = (
            """Help support the communities gameservers and bs operations costs at
            https://www.patreon.com/xhcommunity"""

            "Find out more at the Monthly Community Donor Meeting"
            
        )
        await ctx.send(msg)

    @commands.command()
    async def donations(self, ctx):
        """
        Community donation policiess explained.  
        """
        text = """

**Community Donations**
Community Donations are appreciated but **not** required!  Occasionally we will self host gameservers that have a operating cost.  To maintain these servers we utilize the community donations when necessary.

__Donations Policy__
Do you host a server under the community name?  Sweet ! We know that most of the cost comes out of your own wallet!  We don't want to control that.  However we have been burned in the past, and the moment you list for donations we require a few things to make sure our community name is not abused.  All donations must be reported to the Council monthly.  We only ask that all funds received in the form of donations be utilized specifically for its purpose.  Any donations that exceeds your requirements must be then put into the Community Donations Fund.  

__Accountability__
Donations are a very overlooked item.  Most people don't look into how this is used.  We disagree with this concept as we have witnessed members stealing donations for personal gain.  All money in which anyone donates to group is required to be 100% accounted for.  
The one thing we strive to do is make sure our books are open.  All donations received are added to a community fund controlled by the **Council**.   Any withdrawal from donations requires community approval.  Community meetings are hosted once a month to review the accounts as to eliminate any abuse.

        """
        await ctx.maybe_send_embed(text)


    # @commands.command()
    # async def delegateAll(self, ctx):
    #     """I delegate to **All** the fucking staff. \n **Support Team** and **Council**"""
    #     memlist = []

    #     for m in ctx.guild.get_role(264156088440455168).members:
    #         memlist.append(m)
    #     for m in ctx.guild.get_role(709928089743917066).members:
    #         memlist.append(m)
    #     for m in ctx.guild.get_role(709174224324919326).members:
    #         memlist.append(m)
    #     await ctx.send(random.choice(memlist).mention)

    # @commands.command()
    # async def voluntold(self,ctx):
    #     """I volunteer **Support Team** for the dumb shit.."""
    #     await ctx.send(random.choice(ctx.guild.get_role(727367693996523631).members).mention)

    # @commands.command()
    # async def delegate(self,ctx):
    #     """I delegate to a **Council** member for the dumb shit.."""
    #     await ctx.send(random.choice(ctx.guild.get_role(687186781388537858).members).mention)