import requests

from app.config.base import (
    DISH_LINK,
    DISHES_LINK,
    MENU_LINK,
    MENUS_LINK,
    SERVER_URL,
    SUBMENU_LINK,
    SUBMENUS_LINK,
)


def compare_models_data(excel_data: dict, db_data: dict):
    excel_keys = excel_data.keys()
    db_keys = db_data.keys()

    ids_to_create = set(excel_keys) - set(db_keys)
    ids_to_delete = set(db_keys) - set(excel_keys)
    ids_to_update = set(excel_keys) & set(db_keys)
    return (ids_to_create, ids_to_update, ids_to_delete)


def crud_menus(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for menu_id in ids_to_create:
        url = SERVER_URL + MENUS_LINK
        requests.post(url, json=excel_data[menu_id])

    for menu_id in ids_to_update:
        url = SERVER_URL + MENU_LINK.format(target_menu_id=menu_id)
        requests.patch(url, json=excel_data[menu_id])

    for menu_id in ids_to_delete:
        url = SERVER_URL + MENU_LINK.format(target_menu_id=menu_id)
        requests.delete(url)


def crud_submenus(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for submenu_id in ids_to_create:
        url = SERVER_URL + SUBMENUS_LINK.format(target_menu_id=excel_data[submenu_id]['menu_id'])
        requests.post(url, json=excel_data[submenu_id])

    for submenu_id in ids_to_update:
        url = SERVER_URL + SUBMENU_LINK.format(
            target_menu_id=excel_data[submenu_id]['menu_id'],
            target_submenu_id=submenu_id,
        )
        requests.patch(url, json=excel_data[submenu_id])

    for submenu_id in ids_to_delete:
        url = SERVER_URL + SUBMENU_LINK.format(
            target_menu_id=excel_data[submenu_id]['menu_id'],
            target_submenu_id=submenu_id,
        )
        requests.delete(url)


def crud_dishes(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for dish_id in ids_to_create:
        url = SERVER_URL + DISHES_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id']
        )
        requests.post(url, json=excel_data[dish_id])

    for dish_id in ids_to_update:
        url = SERVER_URL + DISH_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id'],
            dish_id=dish_id
        )
        requests.patch(url, json=excel_data[dish_id])

    for dish_id in ids_to_delete:
        url = SERVER_URL + DISH_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id'],
            dish_id=dish_id
        )
        requests.delete(url)
