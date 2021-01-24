from discord.ext import commands


class WindiaFAQ(commands.Bot):
    def __init__(self, command_prefix, config, intents):
        super().__init__(command_prefix, intents=intents)
        self.config = config

    async def on_ready(self):
        print(f'{self.user} online')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        if ctx.command is None:
            return

        if await self.can_invoke(ctx):
            return await self.invoke(ctx)
        else:
            return await ctx.send('Please use the bot channel.', delete_after=5.0)

    async def can_invoke(self, ctx):
        if not ctx.guild:
            return True

        bot_channel_id = self.config['Bot']['Channel']
        return ctx.channel.id == bot_channel_id \
               or ctx.author.permissions_in(ctx.channel).manage_messages \
               or await self.is_owner(ctx.author)
