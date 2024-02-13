# import json
import logging

import requests
from celery import Celery

from app.celery.helpers.compare import crud_dishes, crud_menus, crud_submenus
from app.celery.helpers.parser import ExcelSheetParser, JsonParser
from app.config.base import (
    ALL_MENUS,
    FILE_PATH,
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
    SERVER_URL,
    SHEET_NAME,
)

app = Celery(
    'tasks',
    broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}'
)


@app.task(max_retries=None, default_retry_delay=15)
def update_db_menu():
    try:
        # parse excel file from admin folder
        excel_parser = ExcelSheetParser(FILE_PATH, SHEET_NAME)
        excel_parser.parse()

        # get json format of db data
        PREVIEW_URL = SERVER_URL + ALL_MENUS
        menu_preview_json = requests.get(PREVIEW_URL).json()

        # parse db data for comparison
        db_parser = JsonParser(menu_preview_json)
        db_parser.parse()

        # crud data in db from excel
        crud_menus(excel_data=excel_parser.menus, db_data=db_parser.menus,)
        crud_submenus(excel_data=excel_parser.submenus, db_data=db_parser.submenus,)
        crud_dishes(excel_data=excel_parser.dishes, db_data=db_parser.dishes,)

    except Exception as error:
        logging.error(error)
    finally:
        update_db_menu.retry()
