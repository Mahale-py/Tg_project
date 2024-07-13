from telebot.types import Message
from peewee import IntegrityError
from models.user import User

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(message, 'Добро пожаловать в менеджер задач!')
    except IntegrityError:
        bot.reply_to(message, f'Рад вас снова видеть, {first_name}!')