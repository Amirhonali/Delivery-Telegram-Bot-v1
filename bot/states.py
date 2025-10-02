from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    choosing_category = State()
    choosing_product = State()