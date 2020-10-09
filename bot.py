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
        await self.invoke(ctx)

    @commands.check
    async def can_invoke(self, ctx):
        bot_channel_id = self.config.getint('Bot', 'Channel')
        return (ctx.guild or ctx.channel.id == bot_channel_id) \
               or ctx.author.permissions_in(ctx.channel).manage_messages \
               or await self.is_owner(ctx.author)
