import asyncio
import logging
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv

from handlers.private_chat import user_pr_router
from keyboards.bot_commands import private
from database.engine import create_db, drop_db

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

ALLOWED_UPDATES = [
    'message',
    'callback_query',
]

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_routers(user_pr_router)


async def main():
    await create_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

    await drop_db()


if __name__ == '__main__':
    try:
        logger.info('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот завершил свою работу')
