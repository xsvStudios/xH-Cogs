import asyncio
import discord

from discord.utils import get
from datetime import datetime, timedelta

from redbot.core import Config, checks, commands
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.antispam import AntiSpam

from redbot.core.bot import Red


class Volunteer(commands.Cog):
    """
    Simple application cog, basically.
    **Use `!volunteersetup` first.**
    """

    __author__ = "saurichable & xBlynd"
    __version__ = "1.1.4"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, 9271530947234, force_registration=True
        )
        self.antispam = {}
        self.config.register_guild(
            applicant_id=None,
            accepter_id=None,
            channel_id=None,
        )

    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_roles=True)
    async def volunteer(self, ctx: commands.Context):
        """Apply to be a staff member."""
        try:
            role_add = get(ctx.guild.roles, id = await self.config.guild(ctx.guild).applicant_id())
        except TypeError:
            role_add = None
        if not role_add:
            role_add = get(ctx.guild.roles, name = "Volunteering")
            if not role_add:
                return await ctx.send("Uh oh, the configuration is not correct. Ask the Admins to set it.")
        try:
            channel = get(ctx.guild.text_channels, id = await self.config.guild(ctx.guild).channel_id())
        except TypeError:
            channel = None
        if not channel:
            channel = get(ctx.guild.text_channels, name = "volunteer applications")
            if not channel:
                return await ctx.send("Uh oh, the configuration is not correct. Ask the Admins to set it.")
        if ctx.guild not in self.antispam:
            self.antispam[ctx.guild] = {}
        if ctx.author not in self.antispam[ctx.guild]:
            self.antispam[ctx.guild][ctx.author] = AntiSpam([(timedelta(days=2), 1)])
        if self.antispam[ctx.guild][ctx.author].spammy:
            return await ctx.send("Uh oh, you're doing this way too frequently.")
        if not role_add:
            return await ctx.send(
                "Uh oh. Looks like your Admins haven't added the required role."
            )
        if not channel:
            return await ctx.send(
                "Uh oh. Looks like your Admins haven't added the required channel."
            )
        try:
            await ctx.author.send(
                """
**Looking to join one of the xH Community Support Teams?**
The roles listed below are currently looking for volunteers.  We have a few questions just to get a little background/info.

**__Moderator Team:__** Volunteers that help monitor and maintain the communities rules and values in our discord.

**__Development Team:__** A group of hobbyist and professionals that assist in gameserver creation, server management, game modding, website development, support the Community Outreach Team, etc.

**__Design Team:__** They make the community look awesome...  The creative members of the community that have talent in the design world and help with logos, website design, gameserver design, support the Community Outreach Team, etc..

**__Community Outreach:__** This group contains the approved community streamers, social media platform team, community youtube content creators, coordinates community Events, giveaways and raffles. 

~~**__Game Server Admins__** - Volunteers to assist in our active game servers.~~ *Coming soon! Check back later.*

Applications will be reviewed by the `xH Community Council`.  A update from the team will be sent to you no longer then 7 days after app is submitted.  *We tend to move faster then this, however life has been difficult for all this year.*

***What position are you applying for?***
*You have maximum of 15 minutes for each following question.*              
                """
            )
        except discord.Forbidden:
            return await ctx.send(
                "I don't seem to be able to DM you. Do you have DM's turned off?"
            )
        await ctx.send(f"Okay, {ctx.author.mention}, i've sent your a DM.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.author.dm_channel

        try:
            position = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send("What is your name?")
        try:
            name = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("You took too long. Try again, please.")
        await ctx.author.send("How old are you?")
        try:
            age = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send("What timezone are you in? (Google is your friend.)")
        try:
            timezone = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send("How many days per week can you be active?")
        try:
            days = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send("How many hours per day can you be active?")
        try:
            hours = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send(
            "Do you have any previous experience? If so, please describe."
        )
        try:
            experience = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        await ctx.author.send("Why do you want to be a member of our team?")
        try:
            reason = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            return await ctx.author.send("```diff\n- You took too long. Try again, please.```")
        embed = discord.Embed(color=await ctx.embed_colour(), timestamp=datetime.now())
        embed.set_author(name="Volunteer Application!", icon_url=ctx.author.avatar_url)
        embed.set_footer(
            text=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})"
        )
        embed.title = (
            f"User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})"
        )
        embed.add_field(name="Name:", value=name.content, inline=True)
        embed.add_field(name="Age:", value=age.content, inline=True)
        embed.add_field(name="Timezone:", value=timezone.content, inline=True)
        embed.add_field(name="Desired position:", value=position.content, inline=True)
        embed.add_field(name="Active days/week:", value=days.content, inline=True)
        embed.add_field(name="Active hours/day:", value=hours.content, inline=True)
        embed.add_field(
            name="Previous experience:", value=experience.content, inline=False
        )
        embed.add_field(name="Reason:", value=reason.content, inline=False)

        await channel.send(embed=embed)

        await ctx.author.add_roles(role_add)

        await ctx.author.send(
            "Thank you, I have sent your application to the team.  As mentioned above I will provide you an update in no later the 7 days."
        )
        self.antispam[ctx.guild][ctx.author].stamp()

    @checks.admin_or_permissions(administrator=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def volunteersetup(self, ctx: commands.Context):
        """Go through the initial setup process."""
        pred = MessagePredicate.yes_or_no(ctx)
        role = MessagePredicate.valid_role(ctx)

        applicant = get(ctx.guild.roles, name="Volunteer Applicant")
        channel = get(ctx.guild.text_channels, name="volunteer applications")

        await ctx.send(
            "This will create required channel and role. Do you wish to continue? (yes/no)"
        )
        try:
            await self.bot.wait_for("message", timeout=30, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again, please.")
        if not pred.result:
            return await ctx.send("Setup cancelled.")
        if not applicant:
            try:
                applicant = await ctx.guild.create_role(
                    name="Volunteering", reason="Application cog setup"
                )
            except discord.Forbidden:
                return await ctx.send(
                    "Uh oh. Looks like I don't have permissions to manage roles."
                )
        if not channel:
            await ctx.send(
                "Do you want everyone to see the applications channel? (yes/no)"
            )
            try:
                await self.bot.wait_for("message", timeout=30, check=pred)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long. Try again, please.")
            if pred.result:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(
                        send_messages=False
                    ),
                    ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                }
            else:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(
                        read_messages=False
                    ),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                }
            try:
                channel = await ctx.guild.create_text_channel(
                    "volunteer applications",
                    overwrites=overwrites,
                    reason="Volunteer cog setup",
                )
            except discord.Forbidden:
                return await ctx.send(
                    "Uh oh. Looks like I don't have permissions to manage channels."
                )
        await ctx.send(f"What role can accept or reject applicants?")
        try:
            await self.bot.wait_for("message", timeout=30, check=role)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again, please.")
        accepter = role.result
        await self.config.guild(ctx.guild).applicant_id.set(applicant.id)
        await self.config.guild(ctx.guild).channel_id.set(channel.id)
        await self.config.guild(ctx.guild).accepter_id.set(accepter.id)
        await ctx.send(
            "You have finished the setup! Please, move your new channel to the category you want it in."
        )

    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_roles=True)
    async def volunteeraccept(self, ctx: commands.Context, target: discord.Member):
        """Accept a volunteer.

        <target> can be a mention or an ID."""
        try:
            accepter = get(ctx.guild.roles, id = await self.config.guild(ctx.guild).accepter_id())
        except TypeError:
            accepter = None
        if not accepter:
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("Uh oh, you cannot use this command.")
        else:
            if accepter not in ctx.author.roles:
                return await ctx.send("Uh oh, you cannot use this command.")
        try:
            applicant = get(ctx.guild.roles, id = await self.config.guild(ctx.guild).applicant_id())
        except TypeError:
            applicant = None
        if not applicant:
            applicant = get(ctx.guild.roles, name="Volunteering")
            if not applicant:
                return await ctx.send("Uh oh, the configuration is not correct. Ask the Admins to set it.")
        role = MessagePredicate.valid_role(ctx)
        if applicant in target.roles:
            await ctx.send(f"What role do you want to accept {target.name} as?")
            try:
                await self.bot.wait_for("message", timeout=30, check=role)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long. Try again, please.")
            role_add = role.result
            try:
                await target.add_roles(role_add)
            except discord.Forbidden:
                return await ctx.send("Uh oh, I cannot give them the role. It might be above all of my roles.")
            await target.remove_roles(applicant)
            await ctx.send(f"Accepted {target.mention} as {role_add}.")
            await target.send(
                f"You have been accepted as {role_add} in {ctx.guild.name}.  A member of the **xH Council** team will be with you shortly for a small briefing."
            )
        else:
            await ctx.send(
                f"Uh oh. Looks like {target.mention} hasn't applied for anything."
            )

    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_roles=True)
    async def volunteerdeny(self, ctx: commands.Context, target: discord.Member):
        """Deny a volunteer.

        <target> can be a mention or an ID"""
        try:
            accepter = get(ctx.guild.roles, id = await self.config.guild(ctx.guild).accepter_id())
        except TypeError:
            accepter = None
        if not accepter:
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("Uh oh, you cannot use this command.")
        else:
            if accepter not in ctx.author.roles:
                return await ctx.send("Uh oh, you cannot use this command.")
        try:
            applicant = get(ctx.guild.roles, id = await self.config.guild(ctx.guild).applicant_id())
        except TypeError:
            applicant = None
        if not applicant:
            applicant = get(ctx.guild.roles, name="Volunteering")
            if not applicant:
                return await ctx.send("Uh oh, the configuration is not correct. Ask the Admins to set it.")
        if applicant in target.roles:
            await ctx.send("Would you like to specify a reason? (yes/no)")
            pred = MessagePredicate.yes_or_no(ctx)
            try:
                await self.bot.wait_for("message", timeout=30, check=pred)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long. Try again, please.")
            if pred.result:
                await ctx.send("Please, specify your reason now.")

                def check(m):
                    return m.author == ctx.author

                try:
                    reason = await self.bot.wait_for(
                        "message", timeout=120, check=check
                    )
                except asyncio.TimeoutError:
                    return await ctx.send("You took too long. Try again, please.")
                await target.send(
                    f"Your application in {ctx.guild.name} has been denied.\n*Reason:* {reason.content}"
                )
            else:
                await target.send(
                    f"Your application in {ctx.guild.name} has been denied."
                )
            await target.remove_roles(applicant)
            await ctx.send(f"Denied {target.mention}'s application.")
        else:
            await ctx.send(
                f"Uh oh. Looks like {target.mention} hasn't applied for anything."
            )
