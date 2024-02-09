import logging
from bot.apps import BotConfig


async def on_startup(dp):
    logging.warning('Starting...')
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    logging.warning('Bye!')
