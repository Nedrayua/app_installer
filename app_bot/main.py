import logging
from aiogram.utils.executor import start_webhook
import os

from bot.bot import bot, dp
from bot import config as conf


FILE_PATH = os.path.dirname(os.path.abspath(__file__))

WEBHOOK_SSL_CERT = os.path.join(FILE_PATH, 'key/bot_cert.pem')

async def on_startup(dp):
    await bot.set_webhook(conf.WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=conf.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=conf.WEBAPP_HOST,
        port=conf.WEBAPP_PORT,
    )
                         
