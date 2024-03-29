import pickle

from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenu as SubMenuSchema
from app.services.main import CacheCRUD


class SubMenuCacheCRUD(CacheCRUD):
    """
    Service for caching endpoints' CRUD operations.\n
    Avaiable methods: `get_submenu`, `set_submenu`, `delete`.
    """

    async def get_submenus(self) -> list[SubMenu] | None:
        """Returns cached list of all submenus if available in cache."""

        if all_submenus := await self.cache.get('all_submenus'):
            return pickle.loads(all_submenus)
        return None

    async def set_submenus(self, query_result: list[dict]) -> None:
        """Sets into cache memory SQLAlchemy query result for getting list of all submenus."""

        await self.cache.set('all_submenus', pickle.dumps(query_result))

    async def invalidate_submenus(self, menu_id: str) -> None:
        """
        Invalidation happens with deleting all related information in cache
        that was anyhow related to all submenus and menus as well as specific menu.
        Made to correctly store valid information at the time PostgreSQL database changes are made.
        """

        await self.cache.delete(
            f'menu_id_{menu_id}',
            'all_submenus',
            'all_menus',
            'menus_preview'
        )

    async def get_submenu(self, submenu_id: str) -> SubMenu | None:
        """Returns cached submenu instance if available."""

        if target_submenu := await self.cache.get(f'submenu_id_{submenu_id}'):
            return pickle.loads(target_submenu)
        return None

    async def set_submenu(self, query_result: SubMenu) -> None:
        """Sets into cache memory SQLAlchemy query result for getting, creating or updating submenu instance."""

        serialized_submenu = SubMenuSchema.model_validate(query_result)
        await self.cache.set(f'submenu_id_{query_result.id}', pickle.dumps(serialized_submenu))

    async def delete(self, submenu_id: str) -> None:
        """Deletes from cache specific submenu instance by its key."""

        await self.cache.delete(f'submenu_id_{submenu_id}')
