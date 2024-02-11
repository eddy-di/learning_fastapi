import pickle

from sqlalchemy import Row

from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.schemas.menu import Menu as MenuSchema
from app.services.main import CacheCRUD


class MenuCacheCRUD(CacheCRUD):

    """
    Service for caching endpoints' CRUD operations.\n
    Avaiable methods: `get_menu`, `set_menu`, `delete`.
    """

    async def get_all(self) -> list[Row[tuple[Menu, SubMenu, Dish]]] | None:
        """Checks if the `everything` key is present/existent in cache db."""

        if everything := self.cache.get('everything'):
            return pickle.loads(everything)
        return None

    async def set_all(
        self,
        query_result: list[Row[tuple[Menu, SubMenu, Dish]]]
    ) -> None:
        """Sets the key `evertyhing` in cache db."""

        self.cache.set('everything', pickle.dumps(query_result))

    async def invalidate_all(self):
        """Executes flushdb command to delete all keys in database without completely killing database"""

        self.cache.flushdb()

    async def get_menus(self) -> list[Menu] | None:
        """Returns cached list of all menus if available in cache."""

        if all_menus := self.cache.get('all_menus'):
            return pickle.loads(all_menus)
        return None

    async def set_menus(self, query_result: list[dict]) -> None:
        """Sets into cache memory SQLAlchemy query result for getting list of all menus."""

        self.cache.set('all_menus', pickle.dumps(query_result))

    async def invalidate_menus(self) -> None:
        """
        Invalidation happens with deleting all related information in cache with all menus.
        Made to correctly store valid information at the time PostgreSQL database changes are made.
        """

        self.cache.delete(
            'all_menus',
            'everything'
        )

    async def get_menu(self, menu_id: str) -> Menu | None:
        """Returns cached menu instance if available."""

        if target_menu := self.cache.get(f'menu_id_{menu_id}'):
            return pickle.loads(target_menu)
        return None

    async def set_menu(self, query_result: Menu) -> None:
        """Sets into cache memory SQLAlchemy query result for getting, creating or updating menu instance."""

        serialized_menu = MenuSchema.model_validate(query_result)
        self.cache.set(f'menu_id_{query_result.id}', pickle.dumps(serialized_menu))

    async def delete(self, menu_id: str) -> None:
        """Deletes from cache specific menu instance by its key."""

        self.cache.delete(f'menu_id_{menu_id}')
