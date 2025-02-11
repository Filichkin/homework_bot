import time
from http import HTTPStatus
from sys import stdout

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
from exceptions import (
    NoVariableError,
    EndpointNotAvailable,
    UnknownHomeworkStatus,
    SendMessageError,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Checks the availability of environment variables."""
    result = True
    for variable in (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID):
        if globals()[variable] is None:
            message = f'Missing of environment variable: {variable}'
            logger.critical(message)
            result = False
            raise NoVariableError(message)
    return result


def send_message(bot, message):
    """Send message to chat."""
    logger.debug('Start of message sending...')
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as mistake:
        message = f'Failed to send message: {mistake}'
        logger.error(message)
        raise SendMessageError(message)
    logger.debug('Message sent successfully')


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
