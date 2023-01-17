import os

from config_reader import config
from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot, storage=storage)
