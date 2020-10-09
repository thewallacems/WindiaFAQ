import re

import discord
from discord.ext import commands

from cogs.utils import calc_magic


class MagicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='magic',
        description='Shows how much magic is needed to one shot a monster with given HP',
        usage='`monster hp` `spell attack` `args: -[alsed]`',
    )
    async def magic_command(self, ctx, hp: int, spell_attack: int, args: str = None):
        modifiers_msg = f'Spell Attack: {spell_attack}\n'
        modifier = 1.0 * spell_attack

        if args:
            if re.search(r'-[^ls]*[ls][^ls]*', args):  # loveless or elemental staff
                modifier *= 1.25
                modifiers_msg += f'Staff Multiplier: 1.25x\n'
            if re.search(r'-[^e]*e[^e]*', args):  # elemental advantage
                modifier *= 1.50
                modifiers_msg += f'Elemental Advantage: 1.50x\n'
            elif re.search(r'-[^d]*d[^d]*', args):  # elemental disadvantage
                modifier *= 0.50
                modifiers_msg += f'Elemental Disadvantage: 0.50x\n'

        magic_msg = ''

        if args and re.search(r'-[^a]*a[^a]*', args):  # elemental amp
            modifiers_msg += f'BW Elemental Amp: 1.30x\n'
            modifiers_msg += f'FP/IL Elemental Amp: 1.40x\n\n'

            # F/P and I/L
            fpil_magic = calc_magic(monster_hp=hp, modifier=modifier * 1.4)
            magic_msg += f'Magic for F/P or I/L: {fpil_magic}\n'

            # BW
            bw_magic = calc_magic(monster_hp=hp, modifier=modifier * 1.3)
            magic_msg += f'Magic for BW: {bw_magic}'
        else:
            magic = calc_magic(monster_hp=hp, modifier=modifier)
            magic_msg += f'\nMagic: {magic}'

        embed = discord.Embed(title='Magic Calculator',
                              description=f'The magic required to one shot a monster with {hp} HP')
        embed.add_field(name='Magic Required', value=magic_msg, inline=True)
        embed.add_field(name='Modifiers', value=modifiers_msg, inline=True)
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @magic_command.error
    async def magic_error(self, ctx, error):
        if error in (commands.MissingRequiredArgument, commands.ArgumentParsingError, commands.ConversionError,
                     commands.TooManyArguments, commands.UserInputError):
            return await ctx.send(
                f'Usage: {self.bot.command_prefix}{ctx.invoked_with} <hp> <spell attack> <args>\n'
                f'Args:\n'
                f'\t-a: Elemental Amplification\n'
                f'\t-l: Loveless Staff\n'
                f'\t-s: Elemental Staff\n'
                f'\t-e: Elemental Advantage\n'
                f'\t-d: Elemental Disadvantage\n\n'
                f'Example Usage: {self.bot.command_prefix}{ctx.invoked_with} 43376970 570 -al'
            )


def setup(bot):
    bot.add_cog(MagicCog(bot))
