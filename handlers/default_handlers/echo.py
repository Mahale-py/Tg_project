from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: True)
def echo_all(message: Message):
    bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, 'Новое сообщение!')