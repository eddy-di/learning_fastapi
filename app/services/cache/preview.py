import pickle

from sqlalchemy import Row

from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.services.main import CacheCRUD


class PreviewCache(CacheCRUD):
    """
    Service caching endpoint showing all avaiable objects in database.
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
