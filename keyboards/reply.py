from enum import StrEnum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class TimeType(StrEnum):
    MORNING = '10:00'
    EVENING = '18:00'


class Period(StrEnum):
    HALF_DAY = "43200"
    ONE_DAY = "86400"


admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить напоминание об пожертвовании", callback_data="send_notificatoins")],
        [InlineKeyboardButton(text="Запустить автонапоминание о пожертвованиях", callback_data="start_notificatoins")],
        [InlineKeyboardButton(text="Остановить автонапоминание о пожертвованиях", callback_data="stop_notificatoins")],
        [InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")],
        [InlineKeyboardButton(text="Удалить админа", callback_data="delete_admin")]
    ]
)

time_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=TimeType.MORNING, callback_data=f'time_type_{TimeType.MORNING}')],
        [InlineKeyboardButton(text=TimeType.EVENING, callback_data=f'time_type_{TimeType.EVENING}')]
    ]
)

period_kb = InlineKeyboardMarkup(
    inline_keyboard= [
        [InlineKeyboardButton(text='12:00', callback_data=f'peroid_type_{Period.HALF_DAY}')],
        [InlineKeyboardButton(text='24:00', callback_data=f'peroid_type_{Period.ONE_DAY}')]
    ]
)

thanks_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Спасибо', callback_data='thanks')]
    ]
)
