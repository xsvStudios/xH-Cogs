import asyncio
import discord 

from redbot.core import Config, checks, commands

from redbot.core.bot import Red

class Devel(commands.Cog):
    """
    This will end of being a Junior Member 
    application for xH Community
    """

    __author = "blynd"
    __version__ = "1.0.1"

    def __init__(self,bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 19882411293845, force_registration=True
        )
        self.config.register_guild(
            junior_member_id=None,
            channel_id=None,
        )


    
    @commands.command()
    async def testy(self, ctx):
        """This does stuff!"""
        # Messing with embeds for a bit.
        text = "This is a embed test?  please work?"
        await ctx.maybe_send_embed(text)

    @checks.admin_or_permissions(administrator=True)
    @commands.command()
    @commands.guild_only()
    # @check.bot_has_permissions(manage_channels=True, manage_rules=True)
    async def appsetup(self, ctx: commands.Context):
        """
        Junior Member app setup.
        """
# Need to add predictions it appears Red has already included this in documentation.
#redbot.core.utils.predicates
        junior_member = get(
            ctx.guild.roles, name='eh Junior Member'
            )
        volunteers = get(
            ctx.guild.roles, name='Volunteer App'
            )
        channel = get(
            ctx.guild.text_channels, name="apps"
            )
        opener_em = discord.Embed(color=0xEE2222, title='xH Community Application')
        embed.add_field(name='Are you setting up for Staff?', value='Hit the ***')
        embed.add_field(name='Are you setting up for Member Apps?', value='Hit the ***')
        embed.set_footer(text='Brought to you by xH Development team')

        await ctx.send(embed=opener_em)