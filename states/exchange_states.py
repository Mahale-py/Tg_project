from telebot.handler_backends import State, StatesGroup


class ExchangeState(StatesGroup):
    asking_for_exchange = State()
    exchange_is_known = State()