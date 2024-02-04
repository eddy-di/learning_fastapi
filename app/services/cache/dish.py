import pickle

from app.models.dish import Dish
from app.schemas.dish import Dish as DishSchema
from app.services.main import CacheCRUD, CacheService


class DishCacheService(CacheService):
    def read_dishes(self):
        if all_dishes := self.cache.get('all_dishes'):
            return pickle.loads(all_dishes)

    def set_dishes(self, query_result: list[Dish]):
        self.cache.set('all_dishes', pickle.dumps(query_result))

    def invalidate_dishes(self, menu_id: str, submenu_id: str):
        self.cache.delete(
            f'menu_id_{menu_id}',
            f'submenu_id_{submenu_id}',
            'all_submenus',
            'all_menus',
            'all_dishes'
        )


class DishCacheCRUD(CacheCRUD):
    def read_dish(self, dish_id):
        if target_dish := self.cache.get(f'dish_id_{dish_id}'):
            return pickle.loads(target_dish)

    def set_dish(self, query_result: Dish):
        serialized_dish = DishSchema.model_validate(query_result)
        self.cache.set(f'dish_id_{query_result.id}', pickle.dumps(serialized_dish))

    def delete(self, dish_id: str):
        self.cache.delete(f'dish_id_{dish_id}')
