from telebot.types import Message
from states.exchange_states import ExchangeState
from config_data.config import ALL_COMMANDS
from loader import bot


@bot.message_handler(state=None, commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}\n' for command, desk in [ALL_COMMANDS[1], ALL_COMMANDS[2], ALL_COMMANDS[3]]]
    bot.reply_to(message, f'Все доступные команды:\n{text}')


@bot.message_handler(state=ExchangeState.exchange_is_known, commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}\n' for command, desk in ALL_COMMANDS]
    bot.reply_to(message, f'Все доступные команды:\n{text}')