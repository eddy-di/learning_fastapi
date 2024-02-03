import os

from dotenv import load_dotenv

load_dotenv()

MENUS_LINK = '/api/v1/menus'
MENU_LINK = '/api/v1/menus/{target_menu_id}'
SUBMENUS_LINK = '/api/v1/menus/{target_menu_id}/submenus'
SUBMENU_LINK = '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}'
DISHES_LINK = '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
DISH_LINK = '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

db_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'

redis_url_connection = f'redis://{REDIS_HOST}'
