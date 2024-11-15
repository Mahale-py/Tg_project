from telebot.types import Message
from models.user import User

from loader import bot


@bot.message_handler(commands=['get_info'])
def get_info(message: Message):
    exchange = 'Bybit'
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    text = (f'Биржа - {exchange}\n'
            f'Никнейм - {username}\n'
            f'Имя - {first_name}\n'
            f'Фамилия - {last_name if last_name is not None else "нет"}\n'
            f'Телеграм-id - {user_id}\n\n'
            f'На данный момент вашей биржей будет только Bybit')

    bot.reply_to(message, text)

