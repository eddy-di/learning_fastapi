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


def get_correct_link(model_name: str, menu_id: str, submenu_id: str | None = None, dish_id: str | None = None):
    if model_name == 'menu':
        return SERVER_URL + MENU_LINK.format(target_menu_id=menu_id)

    if model_name == 'submenu':
        return SERVER_URL + SUBMENU_LINK.format(
            target_menu_id=menu_id,
            target_submenu_id=submenu_id,
        )

    return SERVER_URL + DISH_LINK.format(target_menu_id=menu_id, target_submenu_id=submenu_id, target_dish_id=dish_id,)


def compare_models_data(excel_data: dict, db_data: dict):
    excel_keys = excel_data.keys()
    db_keys = db_data.keys()

    ids_to_create = set(excel_keys) - set(db_keys)
    ids_to_delete = set(db_keys) - set(excel_keys)
    ids_to_update = set(excel_keys) & set(db_keys)
    return (ids_to_create, ids_to_update, ids_to_delete)


def crud_menus(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for id in ids_to_create:
        url = SERVER_URL + MENUS_LINK
        requests.post(url, json=excel_data[id])

    for id in ids_to_update:
        url = get_correct_link(
            model_name='menu',
            menu_id=id,
        )
        requests.patch(url, json=excel_data[id])

    for id in ids_to_delete:
        url = get_correct_link(
            model_name='menu',
            menu_id=id,
        )
        requests.delete(url)


def crud_submenus(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for id in ids_to_create:
        url = SERVER_URL + SUBMENUS_LINK.format(target_menu_id=excel_data[id]['menu_id'])
        requests.post(url, json=excel_data[id])

    for id in ids_to_update:
        url = get_correct_link(
            model_name='submenu',
            menu_id=excel_data[id]['menu_id'],
            submenu_id=id
        )
        requests.patch(url, json=excel_data[id])

    for id in ids_to_delete:
        url = get_correct_link(
            model_name='submenu',
            menu_id=excel_data[id]['menu_id'],
            submenu_id=id
        )
        requests.delete(url)


def crud_dishes(excel_data: dict, db_data: dict):
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    for id in ids_to_create:
        url = SERVER_URL + DISHES_LINK.format(
            target_menu_id=excel_data[id]['menu_id'],
            target_submenu_id=excel_data[id]['submenu_id']
        )
        requests.post(url, json=excel_data[id])

    for id in ids_to_update:
        url = get_correct_link(
            model_name='dish',
            menu_id=excel_data[id]['menu_id'],
            submenu_id=excel_data[id]['submenu_id'],
            dish_id=id
        )
        requests.patch(url, json=excel_data[id])

    for id in ids_to_delete:
        url = get_correct_link(
            model_name='dish',
            menu_id=excel_data[id]['menu_id'],
            submenu_id=excel_data[id]['submenu_id'],
            dish_id=id
        )
        requests.delete(url)
