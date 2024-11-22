from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import SUPPORTABLE_COINS


def gen_markup():
    buttons = []
    keyboard = InlineKeyboardMarkup()
    for coin_name, coin_symbol in SUPPORTABLE_COINS:
        buttons.append((coin_name, coin_symbol))
        if len(buttons) == 2:
            button1 = InlineKeyboardButton(text=buttons[0][0], callback_data=buttons[0][1])
            button2 = InlineKeyboardButton(text=buttons[1][0], callback_data=buttons[1][1])
            keyboard.add(button1, button2)
            buttons = []
    if len(buttons) == 1:
        button = InlineKeyboardButton(text=buttons[0][0], callback_data=buttons[0][1])
        keyboard.add(button)

    cancel_button = InlineKeyboardButton(text='Отмена', callback_data='cancel_currency_choose')
    keyboard.add(cancel_button)
    return keyboard