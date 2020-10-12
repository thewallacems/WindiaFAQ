import os.path
import traceback

from discord.ext import commands

from bot import WindiaFAQ
from intentsloader import IntentsCSVLoader
from configloader import ConfigINILoader

config = ConfigINILoader('windia.ini').load()

token = config['Bot']['Token']
prefix = config['Bot']['Prefix']

intents = IntentsCSVLoader('intents.csv').load()
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
