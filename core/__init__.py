import os
from core.settings import Config
from core.urls import BaseURL

CONFIG_PATH = "./.settings/config.ini"
if not os.access(CONFIG_PATH, os.F_OK):
    raise FileNotFoundError(f"Config {CONFIG_PATH} not found!")

# init singletons
config = Config(CONFIG_PATH)
BaseURL(config['Website']['root'])


