from discord.ext import commands
import sys
import traceback
import sqlite3


class ErrorsCog(commands.Cog):
    __slots__ = ['bot']

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_command_error')
    async def log_command_errors(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.UserInputError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, please follow the command\'s proper usage:\n'
                f'{self.bot.command_prefix}{ctx.invoked_with} {ctx.command.usage}'
            )
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.BotMissingPermissions):
                return await ctx.send(
                    f'**ERROR** I lack permissions to use this command. I need `{error.missing_perms}`.'
                )
            elif isinstance(error, commands.BotMissingRole):
                return await ctx.send(
                    f'**ERROR** I lack the role to use this command. I need `{error.missing_role}`.'
                )
            elif isinstance(error, commands.BotMissingAnyRole):
                return await ctx.send(
                    f'**ERROR** I lack a role to use this command. I need one of any `{error.missing_roles}`.'
                )
            else:
                return await ctx.send(
                    f'**ERROR** {ctx.author.mention}, please use the bot channel.'
                )
        elif isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may only be used in DMs.'
            )
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may not be used in DMs.'
            )
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.'
            )
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, you are on cooldown for {error.retry_after} seconds.'
            )
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.'
            )
        elif isinstance(error, commands.ConversionError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, {error.converter} failed!'
            )
        else:
            if isinstance(error, commands.CommandInvokeError):
                error = error.original
                if isinstance(error, sqlite3.OperationalError):
                    return await ctx.send('That command does not exist.')
                elif isinstance(error, ConnectionError):
                    return await ctx.send('The database is not connected.')

            etype = type(error)
            etb = error.__traceback__
            print(
                f'**COMMAND ERROR**\n',
                f'An unknown or unhandled error has occurred {type(error).__name__}\n',
                f'User Message {ctx.message.content}\n',
                f'Error Message {"".join(traceback.format_exception(etype, error, etb, 4))}'
            )

            return await ctx.send(
                f'**ERROR** An unknown or unhandled error has occurred processing this command.'
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
