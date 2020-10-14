import csv
from abc import ABC, abstractmethod

import discord

_INTENTS = {
    'guilds': False,
    'members': False,
    'bans': False,
    'emojis': False,
    'integrations': False,
    'webhooks': False,
    'invites': False,
    'voice_states': False,
    'presences': False,
    'messages': False,
    'guild_messages': False,
    'dm_messages': False,
    'reactions': False,
    'guild_reactions': False,
    'dm_reactions': False,
    'typing': False,
    'guild_typing': False,
    'dm_typing': False,
}


class IntentsLoader(ABC):
    def __init__(self, file_path: str = 'intents.csv'):
        self.file_path = file_path

    @abstractmethod
    def load(self):
        return


class IntentsCSVLoader(IntentsLoader):
    def load(self):
        if not self.file_path.endswith('.csv'):
            raise ValueError(f'Intents file must be a CSV file.')

        csv_intents = dict()
        intents = discord.Intents.none()

        with open(self.file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_intents[row['intent']] = bool(row['value'])

        intents.guilds = csv_intents['guilds']
        intents.members = csv_intents['members']
        intents.bans = csv_intents['bans']
        intents.emojis = csv_intents['emojis']
        intents.integrations = csv_intents['integrations']
        intents.webhooks = csv_intents['webhooks']
        intents.invites = csv_intents['invites']
        intents.voice_states = csv_intents['voice_states']
        intents.presences = csv_intents['presences']
        intents.messages = csv_intents['messages']
        intents.guild_messages = csv_intents['guild_messages']
        intents.dm_messages = csv_intents['dm_messages']
        intents.reactions = csv_intents['reactions']
        intents.guild_reactions = csv_intents['guild_reactions']
        intents.dm_reactions = csv_intents['dm_reactions']
        intents.typing = csv_intents['typing']
        intents.guild_typing = csv_intents['guild_typing']
        intents.dm_typing = csv_intents['dm_typing']

        return intents
