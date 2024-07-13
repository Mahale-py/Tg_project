from loader import bot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states.exchange_states import ExchangeState
from models.user import User
from config_data.config import ALL_COMMANDS

def gen_markup():
    Binance = KeyboardButton(text='Binance')
    Huobi = KeyboardButton(text='Huobi')
    Coinbase = KeyboardButton(text='Coinbase')
    Kraken = KeyboardButton(text='Kraken')
    Zaif = KeyboardButton(text='Zaif')
    AscendEX = KeyboardButton(text='AscendEX')
    Garantex = KeyboardButton(text='Garantex')
    CoinEx = KeyboardButton(text='CoinEx')
    Bittrex = KeyboardButton(text='Bittrex')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(Binance, Huobi, Coinbase, Kraken, Zaif, AscendEX, Garantex, CoinEx, Bittrex)

    return keyboard


@bot.message_handler(state=None, commands=['change_exchange'])
def ask_for_exchange(message: Message):
    bot.send_message(message.from_user.id,
                     'Ввыберите биржу, в которой собираетесь работать',
                     reply_markup=gen_markup())
    bot.set_state(message.from_user.id, ExchangeState.asking_for_exchange, message.chat.id)


@bot.message_handler(state=ExchangeState.asking_for_exchange)
def change_exchange(message: Message):
    User.exchange = message.text
    new_commands = [f'/{command} - {desk}' for command, desk in ALL_COMMANDS]
    bot.send_message(message.from_user.id,
                     'Спасибо! Теперь вам открыто множество функций, например: \n'
                     '\n'.join(new_commands),
                     reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, ExchangeState.exchange_is_known, message.chat.id)


