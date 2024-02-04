import pickle

from app.models.menu import Menu
from app.services.main import CacheCRUD, CacheService


class MenuCacheService(CacheService):
    def read_menus(self):
        if all_menus := self.cache.get('all_menus'):
            return pickle.loads(all_menus)

    def set_menus(self, query_result: list[dict]):
        self.cache.set('all_menus', pickle.dumps(query_result))

    def invalidate_menus(self):
        self.cache.delete('all_menus')


class MenuCacheCRUD(CacheCRUD):
    def read_menu(self, menu_id: str):
        if target_menu := self.cache.get(f'menu_id_{menu_id}'):
            return pickle.loads(target_menu)

    def set_menu(self, menu_id: str, query_result: Menu):
        self.cache.set(f'menu_id_{menu_id}', pickle.dumps(query_result))

    def create_or_update(self, query_result: Menu):
        self.cache.set(f'menu_id_{query_result.id}', pickle.dumps(query_result))

    def delete(self, menu_id: str):
        self.cache.delete(f'menu_id_{menu_id}')
