from telebot.types import Message
from config_data.config import ALL_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = '\n'.join([f'/{command} - {desk}' for command, desk in ALL_COMMANDS])
    bot.send_message(message.from_user.id, f'Все доступные команды:\n\n{text}')
