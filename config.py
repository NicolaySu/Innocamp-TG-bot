from json import load, dump
from os import path
from sys import exit

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties

CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), "config.json")

# Шаблон конфигурации (на случай, если файл отсутствует)
DEFAULT_CONFIG = {
    "bot_token": "",
    "api_key": "",
    "folder_id": ""
}

# Конфигурация бота
if path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = load(f)
        TOKEN = config["bot_token"]
        API = config["api_key"]
        FOLDER = config["folder_id"]

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='html'))
    dp = Dispatcher()
    rt = Router()

else:  # Создание конфига по шаблону, если он отсутствует
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        dump(DEFAULT_CONFIG, f, indent=4)
    print('JSON не заполнен!!!')
    exit(1)
