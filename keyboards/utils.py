from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database import requests as rq
from database.models import Donate

async def donats_list_kb(row=2, column=3, page=0):
    donats = await rq.get_donats(offset=row*column*page, limit=row*column+1)
    donat_list: List[Donate] = [i for i in donats]

    len_donats:int = len(donat_list)

    keyboard = InlineKeyboardBuilder()

    if len_donats == 0:
        pass
    else:
        for _ in range(row):
            rows = []
            if not donat_list: break
            for _ in range(column):
                if not donat_list: break
                donat = donat_list.pop(0)
                
                rows.append(InlineKeyboardButton(text=donat.title, callback_data=f'donateID:{donat.id}'))
            keyboard.row(*rows)
    
    if len_donats <= row*column:
        pass
    elif len_donats > row*column and page == 0:
        keyboard.row( InlineKeyboardButton(text="▶️", callback_data=f"donate_page:{page+1}") )
    elif len_donats > row*column and page == 2082//(column*row): #Здесь 2082 как костыль стоит, потому что я хотел эффективные запросы делать, а для работы этой функции нужно знать количество сборов на пожертвования, в будущем доделаем
        keyboard.row( InlineKeyboardButton(text="◀️", callback_data=f"donate_page:{page-1}") )
    else:
        keyboard.row(
            InlineKeyboardButton(text="◀️", callback_data=f"donate_page:{page-1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"donate_page:{page+1}")
        )
    
    return keyboard.as_markup()