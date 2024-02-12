import logging

from celery import Celery

from app.config.base import (
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_USER,
)

# from app.services.tasks.parse import ExcelSheetParse

celery = Celery(
    'tasks',
    broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'
)


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_database():
    try:
        # parsed_data: list[dict] = ExcelSheetParse().get_preview_result()
        ...
    except Exception as error:
        logging.error(error)
    finally:
        update_database.retry()
