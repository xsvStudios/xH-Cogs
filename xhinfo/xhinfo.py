
import discord
from redbot.core import commands, checks
from typing import Optional

class xhInfo(command.Cog):
    """ Community Info   """
    __author__ = ["Blynd"]
    __version__ = "1.0,0"

    @commands.command()
    async def ourroles(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("""```md
[Members:](Considered the most important role in the community)
#Tasks: 
    1. Votes on all major community decisions and recruits.
#Role Removal/Ban: 
    1. <Moderator(s)> to review case.
    2. Accused <Member> to defend themselves to <Moderator(s)>.
    3. If <Moderator> deems case just. <Moderator> to submit vote to all <Members> for removal/ban.
    * Majority Vote required

[Council:](Senior Members nominated by the community)
#Tasks
    1. Manage the operations of the Community to continue the growing success.
    2. Manage Support Teams
    3. Update <Members> on changes.
#Removal/Ban
    1. Any case to be reviewed by <Council>.

< Support-Teams >
* Join the team !  Type !apply to join the team.
* Please read the Community guides.  Commands: !rules !modguide !ourroles !policy

[Moderator](Volunteers)
#Tasks
    1. Maintain our rules and policies in discord.
#Role Removal
    1. <Council> to review any case against a <Moderator>

[Development Team](Volunteers)
#Task
    1. Supports the development and outreach of the Community.
#Role Removal
    1. <Council> to review any case against a <Development-Team>

[Game Server Admin](A member that has been approved by the Council to host or admin a Community Gameserver.)
#Task
    1. Uphold the Community values and policies to not tarnish the group.
#Role Removal
    1. <Council> to review any case against a <Server-Admin>

[Trusted Guest](A person deemed trusted to have access to certain channels and voice activation)
#Task
    1. Don't be a dick.
#Role Removal
    1. No case required.  <Moderator> ultimate decision.

[Guests](Just a random person)
#Task
    1. Don't be a dick.
#Kick/Ban
    1. No case required.  <Moderator> ultimate decision.

[GameRoles](Roles created for access to Game channels that are hidden.)
* This role has ZERO value.

```""")