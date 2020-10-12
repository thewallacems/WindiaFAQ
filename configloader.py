from configparser import ConfigParser
from abc import ABC, abstractmethod


def _is_bool(value: str):
    return value.lower() in ('false', 'true', 'yes', 'no')


class ConfigLoader(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def load(self):
        pass


class ConfigINILoader(ConfigLoader):
    def load(self) -> dict:
        config = ConfigParser()
        config.optionxform = str
        config.read(self.file_path)

        config_dict = dict()

        for section in config.sections():
            config_dict[section] = dict()
            for key, value in config.items(section):
                if value.isdigit():
                    config_dict[section][key] = int(value)
                elif _is_bool(value):
                    config_dict[section][key] = bool(value)
                else:
                    config_dict[section][key] = value

        return config_dict
