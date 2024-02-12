import logging

from celery import Celery

# from app.celery.helpers.menu import UpdateMenu
from app.celery.helpers.parser import ExcelSheetParser
from app.config.base import (
    FILE_PATH,
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
    SHEET_NAME,
)

app = Celery(
    'tasks',
    broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}'
)


@app.task(max_retries=None, default_retry_delay=10)
def update_db_menu():
    try:
        parser = ExcelSheetParser(FILE_PATH, SHEET_NAME)
        parser.parse()
        # menu_updater = UpdateMenu(parser.menus)

    except Exception as error:
        logging.error(error)
    finally:
        update_db_menu.retry()
