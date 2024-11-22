from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


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
