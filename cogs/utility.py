from discord.ext import commands
from typing import Optional
from cogs.utils import simulate_ees

import discord
import math


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='id',
        description='Displays your Discord ID to link to Windia',
        usage='`optional user mention`'
    )
    async def id_command(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        return await ctx.send(f'{member.display_name}\'s Discord ID is **{member.id}**. Type `@discord` in game '
                              f'and enter this ID into the prompt to link your in-game account to your Discord account.')

    @commands.command(
        name='online',
        description='Displays the current online count of Windia\'s game server',
        usage='',
    )
    async def online_command(self, ctx):
        windia_guild_id = 610212514856435719
        if not ctx.guild or ctx.guild.id != windia_guild_id:
            return await ctx.send('This command may only be used in the Windia Discord Server.')

        windia_bot_id = 614221348780113920
        windia_bot = ctx.guild.get_member(windia_bot_id)
        if not windia_bot or not windia_bot.activity:
            return await ctx.send('I cannot get the online count currently.')

        online_count = windia_bot.activity.name[-2:]
        return await ctx.send(f'Online Users: {online_count}')

    @commands.command(
        name='ees',
        description='Simulates EES',
        usage='`start-end` `protect delta` `optional samples`'
    )
    async def ees_command(self, ctx, ees: str, protect_delta: int, samples: int = 10_000):
        start, end = map(int, ees.split('-'))
        protect_delta = int(protect_delta)

        if samples > 10_000:
            return await ctx.send(f'{ctx.author.mention}, please keep samples to a maximum of 10,000.')
        elif start < 0 or end > 15:
            return await ctx.send(f'{ctx.author.mention}, stars must be a minimum of 0 and a maximum of 15.')

        message = await ctx.send(f'Running simulation of EES from {start}* to {end}* {samples} times...')
        result = await self.bot.loop.run_in_executor(None, simulate_ees, ees, protect_delta, samples)
        await message.delete()

        ees_meso_cost = 175_000_000
        sfprot_dp_cost = 2_500
        sfprot_vp_cost = 5

        def roundup(x):
            return int(math.ceil(x / 10_000.0)) * 10_000

        embed = discord.Embed(title='EES Simulator', description=result['description'])
        embed.add_field(
            name='EES',
            value=f'Average Used: {result["ees_average"]:,.2f}\nMinimum Used: {result["ees_min"]:,}\nMaximum Used: {result["ees_max"]:,}\n\nAverage Meso Used: {ees_meso_cost * result["ees_average"]:,.2f}\nMinimum Meso Used: {ees_meso_cost * result["ees_min"]:,}\nMaximum Meso Used: {ees_meso_cost * result["ees_max"]:,}'
        )
        embed.add_field(
            name='Starforce Protection Scrolls',
            value=f'Average Used: {result["sfprot_average"]:,.2f}\nMinimum Used: {result["sfprot_min"]:,}\nMaximum Used: {result["sfprot_max"]:,}\n\nAverage VP/Credits Used: {sfprot_vp_cost * result["sfprot_average"]:,.2f}/{roundup(sfprot_dp_cost * result["sfprot_average"]):,}\nMinimum VP/Credits Used: {sfprot_vp_cost * result["sfprot_min"]:,}/{roundup(sfprot_dp_cost * result["sfprot_min"]):,}\nMaximum VP/Credits Used: {sfprot_vp_cost * result["sfprot_max"]:,}/{roundup(sfprot_dp_cost * result["sfprot_max"]):,}'
        )
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)

        return await ctx.send(embed=embed)

    @ees_command.error
    async def ees_error(self, ctx, error):
        if error in (commands.MissingRequiredArgument, commands.ArgumentParsingError, commands.ConversionError,
                     commands.TooManyArguments, commands.UserInputError):
            return await ctx.send(
                f'Usage: {self.bot.command_prefix}{ctx.invoked_with} <start-end> <protect delta> <optional samples>\n'
                f'Protect Delta - how many stars before the checkpoints to start using SF Protection Scrolls '
                f'i.e. 3 will use Star Force Protection scrolls at 2 stars and 7 stars.'
            )


def setup(bot):
    bot.add_cog(UtilityCog(bot))
