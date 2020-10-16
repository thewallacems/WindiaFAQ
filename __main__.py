import os.path
import traceback

from discord.ext import commands

from bot import WindiaFAQ
from configloader import ConfigINILoader
from intentsloader import IntentsCSVLoader

DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(DIR, 'windia.ini')
INTENTS_PATH = os.path.join(DIR, 'intents.csv')
COGS_PATH = os.path.join(DIR, 'cogs')

config = ConfigINILoader(CONFIG_PATH).load()

config['FAQ']['Database'] = f"sqlite:///{os.path.join(DIR, config['FAQ']['Database'])}"
token = config['Bot']['Token']
prefix = config['Bot']['Prefix']

intents = IntentsCSVLoader(INTENTS_PATH).load()
bot = WindiaFAQ(prefix, config, intents)

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
