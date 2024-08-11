from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter
from database import requests as rq 
from keyboards import reply
from states.fsm import AdminAddState, AdminDelState


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]))


@admin_router.message(Command('admin'))
async def admin_panel_call(message: types.Message) -> None:
    if message.from_user.id in (6759351674,) or await rq.check_user_admin(message.from_user.id):
        await message.answer('Панель администратора', reply_markup=reply.admin_kb)
    

@admin_router.callback_query(F.data == "add_admin")
async def add_admin(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in (6759351674,) or await rq.check_user_admin(callback.from_user.id):
        await state.set_state(AdminAddState.tg_id)
        await callback.message.answer("Введите id пользователя которого хотите добавить в администраторы")
    else:
        await callback.message.answer("Недостаточно прав")
    await callback.answer()


@admin_router.message(AdminAddState.tg_id)
async def add_admin_tg_id(message: types.Message, state: FSMContext):
    admin = await rq.set_admin(message.text)
    await state.clear()
    
    if admin: await message.answer('Пользователь теперь администратор')
    else: await message.answer('Пользователь уже администратор')


@admin_router.callback_query(F.data == 'delete_admin')
async def delete_admin(callback: types.CallbackQuery, state: FSMContext):
    if await rq.check_user_admin(callback.from_user.id):
        await state.set_state(AdminDelState.tg_id)
        await callback.message.answer("Введите id пользователя которого хотите удалить из администраторов")
    else:
        await callback.message.answer("Недостаточно прав")
    await callback.answer()
    

@admin_router.message(AdminDelState.tg_id)
async def delete_admin_tg_id(message: types.Message, state: FSMContext):
    admin = await rq.delete_admin(message.text)
    await state.clear()
    
    if admin: await message.answer('Пользователь удален из администраторов')
    else: await message.answer('Пользователь не найден в администраторах')


