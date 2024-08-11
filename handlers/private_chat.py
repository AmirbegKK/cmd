from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from enum import IntEnum, StrEnum

from keyboards import utils
from filters.chat_types import ChatTypeFilter
from database import requests as rq
from states import fsm


user_pr_router = Router()
user_pr_router.message.filter(ChatTypeFilter(["private"]))


class DonateStatus(IntEnum):
    ACTIVE = 4
    FINISHED = 5
    CLOSED = 6


class DonateStatusText(StrEnum):
    ACTIVE = 'Идет сбор средств'
    FINISHED = 'Необходимая сумма уже собрана, сбор завершен'
    CLOSED = 'Сбор закрыт принудительно'


class ReviewType(IntEnum):
    BOT = 1
    APP = 2


@user_pr_router.message(CommandStart())
@user_pr_router.message(F.text.lower() == "старт")
async def start_cmd(message: types.Message) -> None:
    await rq.set_user(message.from_user.id, name=message.from_user.first_name)
    await message.answer("Приветственный текст")


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
async def donate_id_callback(callback: types.CallbackQuery) -> None:
    donate_id = int(callback.data.split(':')[-1])

    donate = await rq.get_donate_by_id(donate_id)
    title = donate.title
    goal = donate.goal
    collected = donate.collected
    publshed_at = donate.published_at
    if donate.status == DonateStatus.ACTIVE:
        status = DonateStatusText.ACTIVE
    elif donate.status == DonateStatus.CLOSED:
        status = DonateStatusText.CLOSED
    elif donate.status == DonateStatus.FINISHED:
        status = DonateStatusText.FINISHED
    finished_at = donate.finished_at if donate.finished_at else "Не окончен"
    text = f'Сбор для: {title}\nСтатус: {status}\nТребуется {goal}\nСобрано: {collected}\nДата начала сбора: {publshed_at}\nДата окончания: {finished_at}\n'

    await callback.message.answer(text)
    await callback.answer()


@user_pr_router.message(Command('review'))
async def review(message: types.Message, command: Command, state: FSMContext) -> None:
    await state.set_state(fsm.ReviewState.text)
    await message.answer('Выберите тип отзыва', reply_markup=utils.review_type_kb())


@user_pr_router.callback_query(F.data.startswith('review_type:'))
async def review_type_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    review_type = int(callback.data.split(':')[-1])
    await state.set_data(data={'review_type': review_type})
    await callback.message.answer('Оставьте ваш отзыв!')


@user_pr_router.message(fsm.ReviewState.text)
async def review_text(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    review_type = state_data['review_type']
    await rq.create_review(tg_id=message.from_user.id, text=message.text, review_type=review_type)
    await message.answer('Спасибо за ваш отзыв! Мы обязательно его учтём.')
    await state.clear()
