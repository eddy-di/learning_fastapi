import os

from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
ALL_MENUS = '/api/v1/menus/preview'
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

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_DEFAULT_PORT = os.getenv('RABBITMQ_DEFAULT_PORT')
RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')

FILE_PATH = 'app/admin/Menu.xlsx'
SHEET_NAME = 'Лист1'

db_url = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
