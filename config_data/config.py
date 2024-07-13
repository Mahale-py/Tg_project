from dotenv import load_dotenv, find_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


ALL_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('change_exchange', 'Поменять/установить биржу'),
    ('show_course', 'Показать курс введенной валюты'),
    ('transfer', 'Перевести из одной валюты в другую')
)

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
)
