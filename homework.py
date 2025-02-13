import json
import time
from http import HTTPStatus
from sys import stdout

import logging
import requests
from telebot import TeleBot

from constants import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    HEADERS,
    RETRY_PERIOD,
    ENDPOINT,
    HOMEWORK_VERDICTS,
)
from exceptions import (
    JsonError,
    NoVariableError,
    EndpointNotAvailable,
    UnknownHomeworkStatus,
    SendMessageError,
)


TOKENS = {
    ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
    ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
}

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Checks the availability of environment variables."""
    tokens_missing = [name for name, token in TOKENS if token is None]
    if tokens_missing:
        message = f'Missing of environment variables: {tokens_missing}'
        logger.critical(message)
        raise NoVariableError(message)


def send_message(bot, message):
    """Send message to chat."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except SendMessageError as error:
        message = f'Failed to send message: {error}'
        logger.error(message)
    else:
        logger.debug(
            f'Message succesfully sent to {TELEGRAM_CHAT_ID}: {message}'
        )


def get_api_answer(timestamp):
    """Makes a request to endpoint."""
    message = 'Endpoint is not available: {}'
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            params=params,
            headers=HEADERS
        )
    except requests.RequestException as error:
        raise EndpointNotAvailable(message.format(error))
    if response.status_code != HTTPStatus.OK:
        raise UnknownHomeworkStatus(
            f'Not succsess status API response: {response.status_code}')
    try:
        return response.json()
    except json.JSONDecodeError as error:
        raise JsonError(
            f'JSON decode error: {error}'
        )


def check_response(response):
    """Checks expected keys in API response."""
    message = 'Response is not belong expected result'
    if not isinstance(response, dict):
        logger.error(message)
        raise TypeError(message)

    if 'current_date' not in response or 'homeworks' not in response:
        logger.error(message)
        raise KeyError(message)

    if not isinstance(response['homeworks'], list):
        logger.error(message)
        raise TypeError(message)


def parse_status(homework):
    """Retrieves homework status."""
    try:
        homework_name = homework['homework_name']
    except KeyError:
        message = 'Key "homework_name" is not available'
        logger.error(message)
        raise KeyError(message)
    try:
        verdict = HOMEWORK_VERDICTS[homework['status']]
    except KeyError:
        message = 'Unknown homework status.'
        logger.error(message)
        raise UnknownHomeworkStatus(message)

    return (f'Изменился статус проверки работы "{homework_name}". {verdict}')


def main():
    """Main logic or the bot."""
    check_tokens()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_error = None
    previous_message = None

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            timestamp = response['current_date']
            homeworks = response['homeworks']
            if not homeworks:
                logger.debug('Empty homework list.')
            else:
                message = parse_status(homeworks[0])
                if previous_message != message:
                    send_message(
                        bot=bot,
                        message=message,
                    )
                    previous_message = message
                else:
                    logger.debug('No updates')

        except Exception as error:
            message = f'Program failure: {error}'
            logger.error(message)
            if error != last_error:
                send_message(
                    bot=bot,
                    message=message
                )
            last_error = error

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
