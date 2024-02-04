import pickle

from app.models.submenu import SubMenu
from app.services.main import CacheCRUD, CacheService


class SubMenuCacheService(CacheService):
    def read_submenus(self):
        if all_submenus := self.cache.get('all_submenus'):
            return pickle.loads(all_submenus)

    def set_submenus(self, query_result: list[dict]):
        self.cache.set('all_submenus', pickle.dumps(query_result))

    def invalidate_submenus(self, menu_id: str):
        self.cache.delete(f'menu_id_{menu_id}')
        self.cache.delete('all_submenus')
        self.cache.delete('all_menus')


class SubMenuCacheCRUD(CacheCRUD):
    def read_submenu(self, submenu_id: str):
        if target_submenu := self.cache.get(f'submenu_id_{submenu_id}'):
            return pickle.loads(target_submenu)

    def set_submenu(self, submenu_id: str, query_result: SubMenu):
        self.cache.set(f'submenu_id_{submenu_id}', pickle.dumps(query_result))

    def create_or_update(self, query_result: SubMenu):
        self.cache.set(f'submenu_id_{query_result.id}', pickle.dumps(query_result))

    def delete(self, submenu_id: str):
        self.cache.delete(f'submenu_id_{submenu_id}')
