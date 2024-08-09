from aiogram import F, Router, types
from aiogram.filters import Command

from keyboards import utils
from filters.chat_types import ChatTypeFilter
from database import requests as rq


user_pr_router = Router()
user_pr_router.message.filter(ChatTypeFilter(["private"]))


@user_pr_router.message(Command('ai_assistent'))
async def ai_assistent_call(message: types.Message, command: Command) -> None:
    await message.answer('Запущен AI-ассистент помогу вам с удобными вопросами.')
    # Add more logic here to handle the command


@user_pr_router.message(Command('donate'))
async def donat_list_call(message: types.Message) -> None:
    kb = await utils.donats_list_kb(row=3, column=2)
    await message.answer('Список пожертвований', reply_markup=kb)


@user_pr_router.callback_query(F.data.startswith('donate_page:'))
async def donate_page_callback(callback: types.CallbackQuery) -> None:
    page = int(callback.data.split(':')[-1])
    kb = await utils.donats_list_kb(row=3, column=2, page=page)
    await callback.message.edit_text('Список пожертвований', reply_markup=kb)
    await callback.answer()


@user_pr_router.callback_query(F.data.startswith('donateID:'))
async def donate_page_callback(callback: types.CallbackQuery) -> None:
    donate_id = int(callback.data.split(':')[-1])

    donate = await rq.get_donate_by_id(donate_id)
    title = donate.title
    goal = donate.goal
    collected = donate.collected
    publshed_at = donate.published_at
    finished_at = donate.finished_at if donate.finished_at else "Не окончен"
    text = f'Сбор для: {title}\nТребуется {goal}\nСобрано: {collected}\nДата начала сбора: {publshed_at}\nДата окончания: {finished_at}\n'

    await callback.message.answer(text)
    await callback.answer()