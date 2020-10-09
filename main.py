import os.path
import traceback
from configparser import ConfigParser

import discord
from discord.ext import commands

from bot import WindiaFAQ

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'windia.ini')
config = ConfigParser()
config.read(CONFIG_PATH)

token = config.get('Bot', 'Token')
prefix = config.get('Bot', 'Prefix')

intents = discord.Intents.none()
intents.members = True
intents.presences = True
intents.messages = True
intents.guilds = True

bot = WindiaFAQ(prefix, config, intents)

COGS_PATH = './cogs/'
cogs = [f'cogs.{file[:-3]}' for file in os.listdir(COGS_PATH) if file.endswith('.py')]

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f'{cog} loaded.')
    except commands.ExtensionAlreadyLoaded:
        print(f'{cog} is already loaded.')
    except commands.ExtensionNotFound:
        print(f'{cog} not found.')
    except commands.NoEntryPointError:
        print(f'{cog} has no setup function.')
    except Exception:
        print(f'An unhandled error was thrown while loading {cog}')
        traceback.print_exc()
        continue

if __name__ == '__main__':
    bot.run(token)
