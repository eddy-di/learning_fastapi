import logging

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


def compare_models_data(excel_data: dict, db_data: dict) -> tuple[set, set, set]:
    """Comparing keys from parsed dict objects to know where to make changes like update, create or delete."""

    excel_keys = excel_data.keys()
    db_keys = db_data.keys()

    ids_to_create = set(excel_keys) - set(db_keys)
    ids_to_delete = set(db_keys) - set(excel_keys)
    ids_to_update = set(excel_keys) & set(db_keys)
    return (ids_to_create, ids_to_update, ids_to_delete)


def crud_menus(excel_data: dict, db_data: dict) -> None:
    """
    Takes result of `compare_models_data` function and performs necessary tasks for menu model and its instances.
    Prioritizing the excel as the main source for CREATE, UPDATE and DELETE operations.
    """

    logging.info('Compare and update menus.')
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    logging.info(f'Menu ids to create: {ids_to_create}.')
    for menu_id in ids_to_create:
        url = SERVER_URL + MENUS_LINK
        requests.post(url, json=excel_data[menu_id])

    logging.info(f'Menu ids to update: {ids_to_update}.')
    for menu_id in ids_to_update:
        url = SERVER_URL + MENU_LINK.format(target_menu_id=menu_id)
        requests.patch(url, json=excel_data[menu_id])

    logging.info(f'Menu ids to delete: {ids_to_delete}.')
    for menu_id in ids_to_delete:
        url = SERVER_URL + MENU_LINK.format(target_menu_id=menu_id)
        requests.delete(url)


def crud_submenus(excel_data: dict, db_data: dict) -> None:
    """
    Takes result of `compare_models_data` function and performs necessary tasks for submenu model and its instances.
    Prioritizing the excel as the main source for CREATE, UPDATE and DELETE operations.
    """

    logging.info('Compare and update submenus.')
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    logging.info(f'Submenu ids to create: {ids_to_create}.')
    for submenu_id in ids_to_create:
        url = SERVER_URL + SUBMENUS_LINK.format(target_menu_id=excel_data[submenu_id]['menu_id'])
        requests.post(url, json=excel_data[submenu_id])

    logging.info(f'Submenu ids to update: {ids_to_update}.')
    for submenu_id in ids_to_update:
        url = SERVER_URL + SUBMENU_LINK.format(
            target_menu_id=excel_data[submenu_id]['menu_id'],
            target_submenu_id=submenu_id,
        )
        requests.patch(url, json=excel_data[submenu_id])

    logging.info(f'Submenu ids to delete: {ids_to_delete}.')
    for submenu_id in ids_to_delete:
        url = SERVER_URL + SUBMENU_LINK.format(
            target_menu_id=excel_data[submenu_id]['menu_id'],
            target_submenu_id=submenu_id,
        )
        requests.delete(url)


def crud_dishes(excel_data: dict, db_data: dict) -> None:
    """
    Takes result of `compare_models_data` function and performs necessary tasks for dish model and its instances.
    Prioritizing the excel as the main source for CREATE, UPDATE and DELETE operations.
    """

    logging.info('Compare and update dishes.')
    ids_to_create, ids_to_update, ids_to_delete = compare_models_data(excel_data, db_data)

    logging.info(f'Dish ids to create: {ids_to_create}.')
    for dish_id in ids_to_create:
        url = SERVER_URL + DISHES_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id']
        )
        requests.post(url, json=excel_data[dish_id])

    logging.info(f'Dish ids to update: {ids_to_update}.')
    for dish_id in ids_to_update:
        url = SERVER_URL + DISH_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id'],
            target_dish_id=dish_id
        )
        requests.patch(url, json=excel_data[dish_id])

    logging.info(f'Dish ids to delete: {ids_to_delete}.')
    for dish_id in ids_to_delete:
        url = SERVER_URL + DISH_LINK.format(
            target_menu_id=excel_data[dish_id]['menu_id'],
            target_submenu_id=excel_data[dish_id]['submenu_id'],
            target_dish_id=dish_id
        )
        requests.delete(url)
