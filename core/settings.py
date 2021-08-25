from configparser import ConfigParser
from core.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self, config_path: str):
        self.parser: ConfigParser = ConfigParser()
        self.parser.read(config_path)

    def __getitem__(self, item):
        return self.parser.__getitem__(item)

    def __iter__(self):
        return self.parser.__iter__()

    def __getattr__(self, item: str):
        return getattr(self.parser, item)


if __name__ == '__main__':
    config = Config("../.settings/config.ini")

    for section in config:
        if section == 'DEFAULT':
            continue
        print(f"[{section}]")
        for setting in config[section]:
            print(f"{setting} = {config[section][setting]}")
        print()
