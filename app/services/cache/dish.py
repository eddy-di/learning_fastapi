import pickle

from app.models.dish import Dish
from app.services.main import CacheCRUD, CacheService


class DishCacheService(CacheService):
    def read_dishes(self):
        if all_dishes := self.cache.get('all_dishes'):
            return pickle.loads(all_dishes)

    def set_dishes(self, query_result: list[Dish]):
        self.cache.set('all_dishes', pickle.dumps(query_result))

    def invalidate_dishes(self, menu_id: str, submenu_id: str):
        self.cache.delete(f'menu_id_{menu_id}')
        self.cache.delete(f'submenu_id_{submenu_id}')
        self.cache.delete('all_submenus')
        self.cache.delete('all_menus')


class DishCacheCRUD(CacheCRUD):
    def read_dish(self, dish_id):
        if target_dish := self.cache.get(f'dish_id_{dish_id}'):
            return pickle.loads(target_dish)

    def set_dish(self, dish_id: str, query_result: Dish):
        self.cache.set(f'dish_id_{dish_id}', pickle.dumps(query_result))

    def create_or_update(self, query_result: Dish):
        self.cache.set(f'dish_id_{query_result.id}', pickle.dumps(query_result))

    def delete(self, dish_id: str):
        self.cache.delete(f'dish_id_{dish_id}')
