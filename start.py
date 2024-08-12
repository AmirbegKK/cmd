import asyncio
import logging

from aiogram import types

from dotenv import find_dotenv, load_dotenv

from main import bot, dp
from handlers.private_chat import user_pr_router
from handlers.admin_chat import admin_router
from keyboards.bot_commands import private
from database.engine import create_db, drop_db
from handlers.shedule import shedule_router


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv(find_dotenv())

ALLOWED_UPDATES = [
    'message',
    'callback_query',
]


dp.include_routers(user_pr_router)
dp.include_routers(admin_router)
dp.include_router(shedule_router)




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
        logger.info('Бот завершил свою работу')
