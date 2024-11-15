from loader import bot
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import SUPPORTABLE_COINS
from handlers.custom_handlers.show_course import get_coin_info, find_pair
from handlers.default_handlers import help


class TransferInfoClass:
    currency1 = None
    currency1_price = None
    currency2 = None
    currency2_price = None


def currency1_choosing():
    buttons = []
    keyboard = InlineKeyboardMarkup()
    for name_and_symbol in SUPPORTABLE_COINS:
        buttons.append(name_and_symbol)
        if len(buttons) == 2:
            button1 = InlineKeyboardButton(
                text=buttons[0][0],  # text = Bitcoin
                callback_data=f'currency1_{buttons[0][1]}'  # callback_data = 'currency1_BTCUSD'
            )
            button2 = InlineKeyboardButton(
                text=buttons[1][0],
                callback_data=f'currency1_{buttons[1][1]}'
            )
            keyboard.add(button1, button2)
            buttons = []
    if len(buttons) == 1:
        button = InlineKeyboardButton(
            text=buttons[0][0],
            callback_data=f'currency1_{buttons[0][1]}'
        )
        keyboard.add(button)

    cancel_button = InlineKeyboardButton(text='Отмена', callback_data='cancel_choosing')
    keyboard.add(cancel_button)

    return keyboard


def currency2_choosing(first_currency_name):
    buttons = []
    keyboard = InlineKeyboardMarkup()
    for name_and_symbol in SUPPORTABLE_COINS:
        if name_and_symbol[0] != first_currency_name:
            buttons.append(name_and_symbol)
            if len(buttons) == 2:
                button1 = InlineKeyboardButton(
                    text=buttons[0][0],  # text = Bitcoin,
                    callback_data=f'currency2_{buttons[0][1]}'  # callback_data = 'transfer_to_BTCUSD'
                )
                button2 = InlineKeyboardButton(
                    text=buttons[1][0],
                    callback_data=f'currency2_{buttons[1][1]}'
                )
                keyboard.add(button1, button2)
                buttons = []
    if len(buttons) == 1:
        button = InlineKeyboardButton(
            text=buttons[0][0],
            callback_data=f'currency2_{buttons[0][1]}'
        )
        keyboard.add(button)

    cancel_button = InlineKeyboardButton(text='Отмена', callback_data='cancel_choosing')
    keyboard.add(cancel_button)

    return keyboard


@bot.message_handler(commands=['transfer'])
def choose_currency1(message: Message):
    bot.send_message(message.from_user.id, 'Выберите первую валюту для сравнения',
                     reply_markup=currency1_choosing())


@bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('currency1_'))
def choose_currency2(callback_query):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data
    TransferInfoClass.currency1 = data[data.rfind('_') + 1:]
    currency1_name = find_pair(TransferInfoClass.currency1)
    bot.send_message(callback_query.from_user.id, f'Вы выбрали {currency1_name}')
    TransferInfoClass.currency1_price = float(
        get_coin_info(
            category='inverse',
            symbol=f'{TransferInfoClass.currency1}')
        ['result']['list'][0]['lastPrice']
    )
    bot.send_message(callback_query.from_user.id, 'Выберите вторую валюту для сравнения',
                     reply_markup=currency2_choosing(first_currency_name=currency1_name))


@bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('currency2_'))
def show_output(callback_query):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data
    TransferInfoClass.currency2 = data[data.rfind('_') + 1:]
    bot.send_message(callback_query.from_user.id, f'Вы выбрали {find_pair(TransferInfoClass.currency2)}')
    TransferInfoClass.currency2_price = float(
        get_coin_info(
            category='inverse',
            symbol=f'{TransferInfoClass.currency2}'
        )['result']['list'][0]['lastPrice']
    )

    price1, sym1 = TransferInfoClass.currency1_price, TransferInfoClass.currency1
    price2, sym2 = TransferInfoClass.currency2_price, TransferInfoClass.currency2

    if price1 > price2:
        text = f'1 {sym1[:sym1.rfind("U")]} ~ {round(price1 / price2, 2)} {sym2[:sym2.rfind("U")]}'
        bot.send_message(callback_query.from_user.id, text)
    if price2 > price1:
        text = f'1 {sym2[:sym2.rfind("U")]} ~ {round(price2 / price1, 2)} {sym1[:sym1.rfind("U")]}'
        bot.send_message(callback_query.from_user.id, text)


@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'cancel_choosing')
def cancel_choosing(callback_query):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    help.bot_help(callback_query)