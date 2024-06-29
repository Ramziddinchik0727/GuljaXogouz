from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterState(StatesGroup):
    get_lang = State()
    full_name = State()
    phone_number = State()


class OrderState(StatesGroup):
    full_name = State()
    phone_number = State()
    location = State()
