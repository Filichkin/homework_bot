import time
from http import HTTPStatus
from typing import NoReturn

import logging
import requests
from telebot import TeleBot, types

from constants import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    RETRY_PERIOD,
    ENDPOINT,
    HEADERS,
    HOMEWORK_VERDICTS,
    )



def check_tokens():
    ...


def send_message(bot, message):
    ...


def get_api_answer(timestamp):
    ...


def check_response(response):
    ...


def parse_status(homework):
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    ...

    # Создаем объект класса бота
    bot = ...
    timestamp = int(time.time())

    ...

    while True:
        try:

            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
        ...


if __name__ == '__main__':
    main()
