from loader import bot
from telebot.types import Message
from pybit.unified_trading import HTTP
import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import SUPPORTABLE_COINS
from handlers.default_handlers import help


def find_pair(tuple_element: str) -> str:
    for currency_name, symbol in SUPPORTABLE_COINS:
        if tuple_element == currency_name:
            return symbol
        if tuple_element == symbol:
            return currency_name


session = HTTP(testnet=True)
get_coin_info = session.get_tickers


class CoinInfoClass:
    cur_coin_info = None


class Currency:
    DOLLAR_RUB = ('https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei'
                  '=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1'
                  '%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044'
                  '.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36'}
    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        return currency


currency = Currency()

rouble_course = int(currency.check_currency())


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


def gen_info_markup():
    keyboard = InlineKeyboardMarkup()

    indexPrice_button = InlineKeyboardButton(text='Индексная цена', callback_data='indexPrice')

    prevPrice24h_button = InlineKeyboardButton(text='Цена сутками ранее', callback_data='prevPrice24h')
    prevPrice1h_button = InlineKeyboardButton(text='Цена часом ранее', callback_data='prevPrice1h')

    highPrice24h_button = InlineKeyboardButton(text='Наивысшая цена за сутки', callback_data='highPrice24h')
    lowPrice24h_button = InlineKeyboardButton(text='Наименьшая цена за сутки', callback_data='lowPrice24h')

    turnover24h_button = InlineKeyboardButton(text='Оборот за сутки', callback_data='turnover24h')
    markPrice_button = InlineKeyboardButton(text='Цена маркировки', callback_data='markPrice')

    price24hPcnt_button = InlineKeyboardButton(text='Процентное изменение цены за сутки', callback_data='price24hPcnt')

    back_button = InlineKeyboardButton(text='Назад', callback_data='back')

    keyboard.add(indexPrice_button)
    keyboard.add(prevPrice24h_button, prevPrice1h_button)
    keyboard.add(highPrice24h_button, lowPrice24h_button)
    keyboard.add(turnover24h_button, markPrice_button)
    keyboard.add(price24hPcnt_button)
    keyboard.add(back_button)

    return keyboard


@bot.message_handler(commands=['show_course'])
def choose_currency(message: Message):
    bot.send_message(message.from_user.id, 'Выберите криптовалюту', reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda callback_query: callback_query.data == callback_query.data.upper())
def show_course(callback_query):
    symbol = callback_query.data
    cur_coin_info = get_coin_info(category='inverse', symbol=f'{symbol}')
    CoinInfoClass.cur_coin_info = cur_coin_info

    price = round(float(cur_coin_info['result']['list'][0]['lastPrice']), 3)
    in_rouble_price = round(rouble_course * price, 4)

    text = (f'Символ - {symbol[:symbol.rfind("U")]}\n'
            f'Последняя цена - {price} $ / {in_rouble_price} ₽\n\n'
            f'(Последняя цена - самая последняя цена, по которой была произведена сделка с ценной бумагой)')

    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, text, reply_markup=gen_info_markup())


@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'cancel_currency_choose')
def cancel(callback_query):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    help.bot_help(callback_query)

# Обработчики кнопок получения информации о монете:
#     show_index_price
#     show_prev_price24h
#     show_prev_price1h
#     show_high_price24h
#     show_low_price24h
#     show_price_24h_pcnt
#     show_turnover_24h
#     back


# Функция show_index_price берет из класса InfoClass список
# данных о монете и берет оттуда значение индексной цены
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'indexPrice')
def show_index_price(callback_query):
    # берем значение из класса InfoClass
    indexPrice = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['indexPrice']), 4)
    in_rouble_price = round(indexPrice * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Индексная цена - {indexPrice} $ / {round(in_rouble_price, 2)} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_prev_price24h берет из класса InfoClass список
# данных о монете и берет оттуда значение цены сутками ранее
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'prevPrice24h')
def show_prev_price24h(callback_query):
    # берем значение из класса InfoClass
    prevPrice24h = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['prevPrice24h']), 4)
    in_rouble_price = round(prevPrice24h * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Цена сутками ранее - {prevPrice24h} $ / {in_rouble_price} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_prev_price1h берет из класса InfoClass список
# данных о монете и берет оттуда значение цены часом ранее
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'prevPrice1h')
def show_prev_price1h(callback_query):
    # берем значение из класса InfoClass
    prevPrice1h = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['prevPrice1h']), 4)
    in_rouble_price = round(prevPrice1h * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Цена часом ранее - {prevPrice1h} $ / {round(in_rouble_price, 2)} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_high_price24h берет из класса InfoClass список
# данных о монете и берет оттуда значение наибольшей цены за сутки
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'highPrice24h')
def show_high_price24h(callback_query):
    # берем значение из класса InfoClass
    highPrice24h = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['highPrice24h']), 4)
    in_rouble_price = round(highPrice24h * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Наивысшая цена за сутки - {highPrice24h} $ / {in_rouble_price} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_low_price24h берет из класса InfoClass список
# данных о монете и берет оттуда значение наименьшей цены за сутки

@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'lowPrice24h')
def show_low_price24h(callback_query):
    # берем значение из класса InfoClass
    lowPrice24h = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['lowPrice24h']), 4)
    in_rouble_price = round(lowPrice24h * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Наименьшая цена за сутки - {lowPrice24h} $ / {in_rouble_price} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_turnover_24h берет из класса InfoClass список
# данных о монете и берет оттуда значение оборота за сутки
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'turnover24h')
def show_turnover_24h(callback_query):
    # берем значение из класса InfoClass
    turnover24h = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['turnover24h']), 4)
    in_rouble_turnover = round(turnover24h * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Оборот за сутки - {turnover24h} $ / {in_rouble_turnover} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_mark_price берет из класса InfoClass список
# данных о монете и берет оттуда значение цены маркировки
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'markPrice')
def show_mark_price(callback_query):
    # берем значение из класса InfoClass
    markPrice = round(float(CoinInfoClass.cur_coin_info['result']['list'][0]['markPrice']), 4)
    in_rouble_price = round(markPrice * rouble_course, 4)
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    text = f'Цена маркировки - {markPrice} $ / {in_rouble_price} ₽   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция show_price_24h_pcnt берет из класса InfoClass список
# данных о монете и берет оттуда значение процентного изменения цены за 24 часа (+/-)
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'price24hPcnt')
def show_price_24h_pcnt(callback_query):
    # берем значение из класса InfoClass
    price24hPcnt = CoinInfoClass.cur_coin_info['result']['list'][0]['price24hPcnt']
    symbol = CoinInfoClass.cur_coin_info['result']['list'][0]['symbol']

    growth = f'+ {price24hPcnt}'
    falling = f'- {price24hPcnt[1:]}'

    text = f'Процентное изменение цены за сутки: {growth if "-" not in str(price24hPcnt) else falling}   ({find_pair(symbol)})'

    bot.send_message(callback_query.from_user.id, text)


# Функция back возвращает пользователя к стадии выбора криптовалюты
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'back')
def back(callback_query):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    choose_currency(callback_query)
