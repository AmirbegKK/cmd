import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
dp = Dispatcher()
bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
