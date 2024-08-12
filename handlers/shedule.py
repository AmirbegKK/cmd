import os
import random as rd

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram import Router

from filters.chat_types import ChatTypeFilter
from handlers.admin_chat import admin_router
from states.fsm import SheduleState
from database import requests as rq 
from keyboards import reply
from main import bot


shedule_router = Router()
shedule_router.message.filter(ChatTypeFilter(["private"]))
ADMIN_ID = int(os.getenv('ADMIN_TG_ID'))
scheduler = AsyncIOScheduler()

notifications_send_acсess = False


date_map= {
    reply.TimeType.MORNING: "10:00",
    reply.TimeType.EVENING: "18:00"
}


@admin_router.callback_query(F.data == 'send_notificatoins')
async def send_notificatoins(*args):
    user_id = await rq.get_users_id()
    
    donate_count = rd.randint(20, 50)
    donates = await rq.get_rand_donate(donate_count)
    
    for user in user_id:
        await bot.send_message(user, f'Напоминаем вам о важности пожертвований и предлагаем данный сбор: \n{donates[rd.randint(1, donate_count)-1].title}')
        

@admin_router.callback_query(F.data == 'start_notificatoins')
async def start_notifications(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        await state.set_state(SheduleState.time)
        await bot.send_message(callback.from_user.id, 'Выберите время для запуска рассылки', reply_markup=reply.time_kb)
        await callback.answer()
    else:
        await callback.message.answer('Недостаточно прав')


@admin_router.callback_query(SheduleState.time)
@admin_router.callback_query(F.data.startswith('time_type_'))
async def set_shedule_time(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        time = callback.data.split('_')[-1]
        await state.update_data(time=time)
        await state.set_state(SheduleState.period)
        await callback.message.answer('Выберите период', reply_markup=reply.period_kb)
        await callback.answer()
         

@admin_router.callback_query(F.data.startswith('peroid_type_'))
async def set_shedule_period(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        period = int(callback.data.split('_')[-1])
        global notifications_send_acсess
        notifications_send_acсess = True

        data = await state.get_data()
        hour=(data['time'])[0:2]
        minute=data['time'][3:5]
        
        if period == 43200:
            scheduler.add_job(
                send_notificatoins, 
                'cron',
                hour=hour,
                minute=minute
            )
            hour = str(int(hour) + 12)
            if int(hour) >= 24: hour = str(int(hour)-24)
            scheduler.add_job(
                send_notificatoins,
                'cron',
                hour=hour,
                minute=minute
            )
        else:
            scheduler.add_job(send_notificatoins, 
                    'cron',
                    hour=hour,
                    minute=minute
                    )
        try:
            scheduler.start()
        except:
            await bot.send_message(callback.from_user.id, 'Автонапоминание уже запущено')
            await callback.answer()
            return

        await callback.message.answer('Время уведомлений установлено')
        await state.clear()
        await callback.answer()


@admin_router.callback_query(F.data == 'stop_notificatoins')
async def stop_notifications(callback: types.CallbackQuery):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        global notifications_send_acсess
        notifications_send_acсess = False
        scheduler.shutdown()
        await bot.send_message(callback.from_user.id, 'Уведомления о сборах остановлены')
        await callback.answer()
    else:
        await callback.message.answer('Недостаточно прав')
