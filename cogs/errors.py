import sqlite3
import sys
import traceback

from discord.ext import commands


class ErrorsCog(commands.Cog):
    __slots__ = ['bot']

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_command_error')
    async def log_command_errors(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.UserInputError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, please follow the command\'s proper usage:\n'
                f'{self.bot.command_prefix}{ctx.invoked_with} {ctx.command.usage}', delete_after=5.0
            )
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.BotMissingPermissions):
                return await ctx.send(
                    f'**ERROR** I lack permissions to use this command. I need `{error.missing_perms}`.', delete_after=5.0
                )
            elif isinstance(error, commands.BotMissingRole):
                return await ctx.send(
                    f'**ERROR** I lack the role to use this command. I need `{error.missing_role}`.', delete_after=5.0
                )
            elif isinstance(error, commands.BotMissingAnyRole):
                return await ctx.send(
                    f'**ERROR** I lack a role to use this command. I need one of any `{error.missing_roles}`.', delete_after=5.0
                )
            else:
                return await ctx.send(
                    f'**ERROR** {ctx.author.mention}, please use the bot channel.', delete_after=5.0
                )
        elif isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may only be used in DMs.', delete_after=5.0
            )
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may not be used in DMs.', delete_after=5.0
            )
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.', delete_after=5.0
            )
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, you are on cooldown for {error.retry_after} seconds.', delete_after=5.0
            )
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.', delete_after=5.0
            )
        elif isinstance(error, commands.ConversionError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, {error.converter} failed!', delete_after=5.0
            )
        else:
            if isinstance(error, commands.CommandInvokeError):
                error = error.original
                if isinstance(error, sqlite3.OperationalError):
                    return await ctx.send('That command does not exist.', delete_after=5.0)
                elif isinstance(error, ConnectionError):
                    return await ctx.send('The database is not connected.', delete_after=5.0)

            etype = type(error)
            etb = error.__traceback__
            print(
                f'**COMMAND ERROR**\n',
                f'An unknown or unhandled error has occurred {type(error).__name__}\n',
                f'User Message {ctx.message.content}\n',
                f'Error Message {"".join(traceback.format_exception(etype, error, etb, 4))}'
            )

            return await ctx.send(
                f'**ERROR** An unknown or unhandled error has occurred processing this command.', delete_after=5.0
            )

    @commands.Cog.listener('on_error')
    async def log_error(self, event_method: str, *args, **kwargs):
        etype, value, tb = sys.exc_info()
        print(
            '**ERROR**\n',
            f'An unknown or unhandled error in {event_method} has occurred\n',
            f'Error Message: ```{"".join(traceback.format_exception(etype, value, tb))}```'
        )


def setup(bot):
    bot.add_cog(ErrorsCog(bot))
