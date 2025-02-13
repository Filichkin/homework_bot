import os

from dotenv import load_dotenv


load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

TOKENS = {
    ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
    ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
}

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
