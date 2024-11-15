from dotenv import load_dotenv, find_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


ALL_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('get_info', 'Вывести вашу информацию'),
    ('show_course', 'Показать курс выбранной валюты'),
    ('transfer', 'Сравнить две валюты')
)

SUPPORTABLE_COINS = (
    ('Bitcoin', 'BTCUSDT'), ('Binance Coin', 'BNBUSDT'),
    ('Cardano', 'ADAUSDT'), ('Ethereum', 'ETHUSD'),
    ('Filecoin', 'FILUSDT'), ('Jito', 'JTOUSDT'),
    ('Litecoin', 'LTCUSD'), ('Mantle Network', 'MNTUSDT'),
    ('Notcoin', 'NOTUSDT'), ('Ondo', 'ONDOUSDT'),
    ('Ordinals', 'ORDIUSDT'), ('Ripple', 'XRPUSD'),
    ('Solana', 'SOLUSD'), ('Stellar Lumens', 'XLMUSDT')
)

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
)
