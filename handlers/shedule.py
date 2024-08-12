import os
import random as rd

from apscheduler.schedulers import SchedulerAlreadyRunningError
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
async def send_notificatoins(callback: types.CallbackQuery=None,*args):
    user_id = await rq.get_users_id()
    
    donates, donate_count = await rq.get_rand_donate()
    
    if callback:
        await callback.answer()
    
    for user in user_id:
        kb = reply.donate_random_kb
        await bot.send_message(user, f'Напоминаем вам о важности пожертвований и предлагаем данный сбор: \n{donates[rd.randint(0, donate_count-1)].title}', reply_markup=kb)
        

@admin_router.callback_query(F.data == 'start_notificatoins')
async def start_notifications(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.from_user.id):
        await state.set_state(SheduleState.time)
        await callback.message.edit_text('Выберите время для запуска рассылки', reply_markup=reply.time_kb)
    else:
        await callback.message.answer('Недостаточно прав')


@admin_router.callback_query(SheduleState.time)
@admin_router.callback_query(F.data.startswith('time_type_'))
async def set_shedule_time(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        time = callback.data.split('_')[-1]
        await state.update_data(time=time)
        await state.set_state(SheduleState.period)
        await callback.message.edit_text('Выберите период', reply_markup=reply.period_kb)
         

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
            if int(hour) >= 24:
                hour = str(int(hour)-24)
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
        except SchedulerAlreadyRunningError:
            await callback.message.edit_text('Автонапоминание уже запущено')
            return

        await callback.message.edit_text('Время уведомлений установлено')
        await state.clear()


@admin_router.callback_query(F.data == 'stop_notificatoins')
async def stop_notifications(callback: types.CallbackQuery):
    if callback.from_user.id == ADMIN_ID or await rq.check_user_admin(callback.message.from_user.id):
        global notifications_send_acсess
        notifications_send_acсess = False
        scheduler.shutdown()
        await callback.message.edit_text(callback.from_user.id, 'Уведомления о сборах остановлены')
    else:
        await callback.message.edit_text('Недостаточно прав')
