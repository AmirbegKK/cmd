from aiogram.fsm.state import State, StatesGroup

class ReviewState(StatesGroup):
    text = State()


class AdminAddState(StatesGroup):
    tg_id = State()


class AdminDelState(StatesGroup):
    tg_id = State()


class SheduleState(StatesGroup):
    time = State()
    period = State()