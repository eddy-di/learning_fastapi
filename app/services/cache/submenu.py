import pickle

from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenu as SubMenuSchema
from app.services.main import CacheCRUD, CacheService


class SubMenuCacheService(CacheService):

    """
    Service for caching submenu endpoint that handles all submenus list output.\n
    Available methods: `read_submenus`, `set_submenus`, `invalidate_submenus`.
    """

    def read_submenus(self) -> list[SubMenu] | None:
        """Returns cached list of all submenus if available in cache."""

        if all_submenus := self.cache.get('all_submenus'):
            return pickle.loads(all_submenus)
        return None

    def set_submenus(self, query_result: list[dict]) -> None:
        """Sets into cache memory SQLAlchemy query result for getting list of all submenus."""

        self.cache.set('all_submenus', pickle.dumps(query_result))

    def invalidate_submenus(self, menu_id: str) -> None:
        """
        Invalidation happens with deleting all related information in cache
        that was anyhow related to all submenus and menus as well as specific menu.
        Made to correctly store valid information at the time PostgreSQL database changes are made.
        """

        self.cache.delete(
            f'menu_id_{menu_id}',
            'all_submenus',
            'all_menus'
        )


class SubMenuCacheCRUD(CacheCRUD):

    """
    Service for caching endpoints' CRUD operations.\n
    Avaiable methods: `read_submenu`, `set_submenu`, `delete`.
    """

    def read_submenu(self, submenu_id: str) -> SubMenu | None:
        """Returns cached submenu instance if available."""

        if target_submenu := self.cache.get(f'submenu_id_{submenu_id}'):
            return pickle.loads(target_submenu)
        return None

    def set_submenu(self, query_result: SubMenu) -> None:
        """Sets into cache memory SQLAlchemy query result for getting, creating or updating submenu instance."""

        serialized_submenu = SubMenuSchema.model_validate(query_result)
        self.cache.set(f'submenu_id_{query_result.id}', pickle.dumps(serialized_submenu))

    def delete(self, submenu_id: str) -> None:
        """Deletes from cache specific submenu instance by its key."""

        self.cache.delete(f'submenu_id_{submenu_id}')
