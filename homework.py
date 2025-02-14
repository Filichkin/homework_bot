import json
import sys
import time
from http import HTTPStatus

import logging
import requests
from telebot import TeleBot

from constants import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    RETRY_PERIOD,
    ENDPOINT,
    HOMEWORK_VERDICTS,
)
from exceptions import (
    JsonError,
    EndpointNotAvailable,
    NoVariableError,
    UnknownHomeworkStatus,
)


TOKENS = ['PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID']
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Checks the availability of environment variables."""
    missing_tokens = [token for token in TOKENS if not globals()[token]]
    if missing_tokens:
        message = f'Missing of environment variables: {missing_tokens}'
        logger.critical(message)
        raise NoVariableError(message)


def send_message(bot, message):
    """Send message to chat."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        message = f'Failed to send message: {error}'
        logger.error(message)
    else:
        logger.debug(
            f'Message succesfully sent to {TELEGRAM_CHAT_ID}: {message}'
        )


def get_api_answer(timestamp):
    """Makes a request to endpoint."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            params=params,
            headers=HEADERS
        )
        if response.status_code != HTTPStatus.OK:
            raise UnknownHomeworkStatus(
                f'Not succsess status API response: {response.status_code}')
        return response.json()
    except requests.RequestException as error:
        raise EndpointNotAvailable(
            f'Endpoint is not available: {error}'
        )
    except json.JSONDecodeError as error:
        raise JsonError(
            f'JSON decode error: {error}'
        )


def check_response(response):
    """Checks expected keys in API response."""
    if not isinstance(response, dict):
        raise TypeError(
            f'Incorrect response format: {type(response)}\n'
            f'Message: {response}'
        )

    if 'current_date' not in response or 'homeworks' not in response:
        raise KeyError('Missing required keys')
    homeworks = response['homeworks']
    current_date = response['current_date']
    if not isinstance(current_date, int):
        logger.debug(
            f'Unexpected value type for key {current_date}, '
            f'received {type(current_date)}.'
        )
    if not isinstance(homeworks, list):
        raise TypeError(f'Response is not list, received {type(homeworks)}.')
    return homeworks


def parse_status(homework):
    """Retrieves homework status."""
    if 'homework_name' not in homework:
        raise KeyError('Key "homework_name" is not available')
    if 'status' not in homework:
        raise KeyError('Key "status" is not available')
    homework_name = homework['homework_name']
    status = homework['status']
    if status not in HOMEWORK_VERDICTS:
        raise UnknownHomeworkStatus(f'{status} is not available')
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Main logic or the bot."""
    check_tokens()
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previous_status = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            timestamp = response['current_date']
            if not homeworks:
                message = 'No new homeworks statuses.'
                logger.debug(message)
            else:
                status = parse_status(homeworks[0])
                if previous_status != status:
                    send_message(bot, status)
                previous_status = status
                logger.debug(status)

        except Exception as error:
            message = f'Bot program failure: {error}'
            if previous_status != message:
                send_message(bot, message)
            previous_status = message
            logger.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
