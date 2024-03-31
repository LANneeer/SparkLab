import logging

from aiogram import Router, exceptions
from aiogram.types import ErrorEvent

router = Router(name='error')


@router.error()
async def errors_handler(event: ErrorEvent):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    exception = event.exception
    update = event.update

    if isinstance(exception, exceptions.DetailedAiogramError):
        logging.warning(f'DetailedAiogramError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramAPIError):
        logging.warning(f'TelegramAPIError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramNetworkError):
        logging.warning(f'TelegramNetworkError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramRetryAfter):
        logging.warning(
            f'TelegramRetryAfter error: {exception}. Retry after {exception.retry_after} seconds. Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramBadRequest):
        logging.warning(f'TelegramBadRequest error: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramUnauthorizedError):
        logging.warning(f'TelegramUnauthorizedError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramForbiddenError):
        logging.warning(f'TelegramForbiddenError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.TelegramServerError):
        logging.warning(f'TelegramServerError: {exception}, Update: {update.update_id}')
        return True

    if isinstance(exception, exceptions.ClientDecodeError):
        logging.warning(f'ClientDecodeError: {exception}, Update: {update.update_id}')
        return True

    logging.exception(f'Unexpected error: {exception}, Update: {update.update_id}')
