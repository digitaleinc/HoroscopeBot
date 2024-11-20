from aiogram.fsm.state import State, StatesGroup

class TarotState(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()

class HoroscopeState(StatesGroup):
    step_1 = State()
    step_2 = State()
