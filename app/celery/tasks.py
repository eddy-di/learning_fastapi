# import json
import logging

import requests
from celery import Celery

from app.celery.helpers.parser import ExcelSheetParser
from app.config.base import (  # ALL_MENUS,
    DISH_LINK,
    DISHES_LINK,
    FILE_PATH,
    MENU_LINK,
    MENUS_LINK,
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
    SERVER_URL,
    SHEET_NAME,
    SUBMENU_LINK,
    SUBMENUS_LINK,
)

app = Celery(
    'tasks',
    broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}'
)


@app.task(max_retries=None, default_retry_delay=15)
def update_db_menu():
    try:
        parser = ExcelSheetParser(FILE_PATH, SHEET_NAME)
        preview_results = parser.parse()
        menus_results = parser.menus
        # submenus_results = parser.submenus
        # dishes_results = parser.dishes

        # PREVIEW_URL = SERVER_URL + ALL_MENUS
        # menu_preview_json = requests.get(PREVIEW_URL).json()
        # menu_preview = json.loads(menu_preview_json)

        # print(preview_results)
        # if preview_results == menu_preview:
        # print("IF PASSED")
        for menu in preview_results:
            MENU_URL = MENU_LINK.format(
                target_menu_id=menu['id'],
            )
            response = requests.get(SERVER_URL + MENU_URL)
            if response.status_code == 404:
                new_menu_data = {
                    'id': menu['id'],
                    'title': menu['title'],
                    'description': menu['description']
                }
                requests.post(SERVER_URL + MENUS_LINK, json=new_menu_data)

            for submenu in menu['submenus']:
                SUBMENU_URL = SUBMENU_LINK.format(
                    target_menu_id=menu['id'],
                    target_submenu_id=submenu['id'],
                )
                response = requests.get(SERVER_URL + SUBMENU_URL)
                if response.status_code == 404:
                    SUBMENUS_URL = SUBMENUS_LINK.format(
                        target_menu_id=menu['id'],
                    )
                    new_submenu_data = {
                        'id': submenu['id'],
                        'title': submenu['title'],
                        'description': submenu['description']
                    }
                    requests.post(SERVER_URL + SUBMENUS_URL, json=new_submenu_data)

                for dish in submenu['dishes']:
                    DISH_URL = DISH_LINK.format(
                        target_menu_id=menu['id'],
                        target_submenu_id=submenu['id'],
                        target_dish_id=dish['id'],
                    )
                    response = requests.get(SERVER_URL + DISH_URL)
                    if response.status_code == 404:
                        DISHES_URL = DISHES_LINK.format(
                            target_menu_id=menu['id'],
                            target_submenu_id=submenu['id'],
                        )
                        new_dish_data = {
                            'id': dish['id'],
                            'title': dish['title'],
                            'description': dish['description'],
                            'price': dish['price'],
                            'discount': dish['discount'],
                        }
                        requests.post(SERVER_URL + DISHES_URL, json=new_dish_data)

        for menu in menus_results:
            for submenu in menu['submenus']:
                for dish in submenu['dishes']:
                    if dish['discount'] > 0:
                        DISH_PATCH_URL = SERVER_URL + DISH_LINK.format(
                            target_menu_id=menu['id'],
                            target_submenu_id=submenu['id'],
                            target_dish_id=dish['id']
                        )
                        dish_patch_data = {
                            'discount': dish['discount']
                        }
                        requests.patch(DISH_PATCH_URL, json=dish_patch_data)

    except Exception as error:
        logging.error(error)
    finally:
        update_db_menu.retry()
