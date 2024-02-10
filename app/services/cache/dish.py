import pickle

from app.models.dish import Dish
from app.schemas.dish import Dish as DishSchema
from app.services.main import CacheCRUD


class DishCacheCRUD(CacheCRUD):

    """
    Service for caching endpoints' CRUD operations.\n
    Avaiable methods: `get_dish`, `set_dish`, `delete`.
    """

    async def get_dishes(self) -> list[Dish] | None:
        """Returns cached list of all dishes if available in cache."""

        if all_dishes := self.cache.get('all_dishes'):
            return pickle.loads(all_dishes)
        return None

    async def set_dishes(self, query_result: list[Dish]) -> None:
        """Sets into cache memory SQLAlchemy query result for getting list of all dishes."""

        self.cache.set('all_dishes', pickle.dumps(query_result))

    async def invalidate_dishes(self, menu_id: str, submenu_id: str) -> None:
        """
        Invalidation happens with deleting all related information in cache
        that was anyhow related to all dishes, submenus and menus as well as specific submenu and menu.
        Made to correctly store valid information at the time PostgreSQL database changes are made.
        """

        self.cache.delete(
            f'menu_id_{menu_id}',
            f'submenu_id_{submenu_id}',
            'all_submenus',
            'all_menus',
            'all_dishes'
        )

    async def get_dish(self, dish_id) -> Dish | None:
        """Returns cached dish instance if available."""

        if target_dish := self.cache.get(f'dish_id_{dish_id}'):
            return pickle.loads(target_dish)
        return None

    async def set_dish(self, query_result: Dish) -> None:
        """Sets into cache memory SQLAlchemy query result for getting, creating or updating dish instance."""

        serialized_dish = DishSchema.model_validate(query_result)
        self.cache.set(f'dish_id_{query_result.id}', pickle.dumps(serialized_dish))

    async def delete(self, dish_id: str) -> None:
        """Deletes from cache specific dish instance by its key."""

        self.cache.delete(f'dish_id_{dish_id}')
