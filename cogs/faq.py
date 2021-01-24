import asyncio

from discord.ext import commands

from cogs.utils import FAQDatabase


class FAQCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = FAQDatabase(bot.config['FAQ']['Database'])

    @commands.command(
        name='add',
        description='Adds a FAQ command',
        usage='`command` `description`',
        hidden=True
    )
    async def add_command(self, ctx, command: commands.clean_content, *, description: commands.clean_content):
        await self.db.create(command, description)
        return await ctx.send(f'{command} added.')

    @commands.command(
        name='update',
        description='Updates an existing FAQ command',
        usage='`command` `new description`',
        hidden=True
    )
    async def update_command(self, ctx, command: commands.clean_content, *, description: commands.clean_content):
        await self.db.update(command, description)
        return await ctx.send(f'{command} updated.')

    @commands.command(
        name='delete',
        description='Deletes an existing FAQ command',
        usage='`command`',
        hidden=True,
    )
    async def delete_command(self, ctx, command: commands.clean_content):
        await self.db.delete(command)
        return await ctx.send(f'{command} deleted.')

    @commands.Cog.listener('on_message')
    async def faq_handler(self, message):
        if message.author.bot:
            return

        content = message.content
        if not content.startswith(self.bot.command_prefix):
            return

        command = content[len(self.bot.command_prefix):].split(' ')[0]
        if self.bot.get_command(command):
            return

        if not self.db.is_connected():
            await self.db.connect()

        resp = await self.db.request(command)
        if not resp:
            return

        windia_guild_id = 610212514856435719
        if message.guild and message.guild.id == windia_guild_id:
            if message.channel.id != self.bot.config['Bot']['Channel']:
                if not await self._is_elevated_user(message.channel, message.author):
                    return await message.channel.send('Please use the bot channel.', delete_after=5.0)

        if isinstance(resp, str):
            return await message.channel.send(resp)
        elif isinstance(resp, list):
            return await message.channel.send(f'Did you mean... {", ".join(resp)}')

    async def cog_before_invoke(self, ctx):
        if not self.db.is_connected():
            await self.db.connect()

    def cog_unload(self):
        asyncio.run(self.db.disconnect())

    async def cog_check(self, ctx):
        if not ctx.guild:
            return False

        return await self._is_elevated_user(ctx.channel, ctx.author)

    async def _is_elevated_user(self, channel, author):
        return author.permissions_in(channel).manage_messages \
               or await self.bot.is_owner(author)


def setup(bot):
    bot.add_cog(FAQCog(bot))
