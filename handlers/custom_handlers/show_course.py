from loader import bot
from states.exchange_states import ExchangeState
from telebot.types import Message
import webbrowser as wb
from models.user import User


@bot.message_handler(state=ExchangeState.exchange_is_known, commands=['show_course'])
def show_course(message: Message):
    ...


