from aiogram.dispatcher.filters.state import StatesGroup, State

class FormAnswer(StatesGroup):
    change_name = State()
    change_phone = State()
    change_email = State()
    change_city = State()
