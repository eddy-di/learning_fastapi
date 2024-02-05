from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.menu import Menu as MenuModel
from app.schemas.menu import MenuCreate as MenuCreateSchema
from app.schemas.menu import MenuUpdate as MenuUpdateSchema
from app.services.cache.menu import MenuCacheCRUD, MenuCacheService
from app.services.database.menu import MenuCRUD
from app.services.main import AppService


class MenuService(AppService):
    """Service for querying the list of all menus."""

    def get_menus(self) -> list[MenuModel] | list[dict]:
        """Query to get list of all menus."""

        if all_menus := MenuCacheService(self.cache).get_menus():
            return all_menus

        result = MenuCRUD(self.db).get_menus()

        MenuCacheService(self.cache).set_menus(query_result=result)

        return result

    def get_menu(self, menu_id: str) -> MenuModel:
        """GET operation for specific menu"""
        if target_menu := MenuCacheCRUD(self.cache).get_menu(menu_id=menu_id):
            return target_menu

        result = MenuCRUD(self.db).get_menu(menu_id=menu_id)

        MenuCacheCRUD(self.cache).set_menu(query_result=result)

        return result

    def create_menu(
        self,
        menu_schema: MenuCreateSchema
    ) -> MenuModel:
        """POST operation for creating menu"""

        result = MenuCRUD(self.db).create_menu(menu_schema=menu_schema)

        MenuCacheCRUD(self.cache).set_menu(query_result=result)

        MenuCacheService(self.cache).invalidate_menus()

        return result

    def update_menu(
        self,
        menu_id: str,
        menu_schema: MenuUpdateSchema,
    ) -> MenuModel | HTTPException:
        """PATCH operation for specific menu"""

        result = MenuCRUD(self.db).update_menu(
            menu_id=menu_id,
            menu_schema=menu_schema
        )

        MenuCacheCRUD(self.cache).set_menu(query_result=result)

        MenuCacheService(self.cache).invalidate_menus()

        return result

    def delete_menu(
        self,
        menu_id: str,
    ) -> JSONResponse:
        """DELETE operation for specific menu"""

        MenuCRUD(self.db).delete_menu(menu_id=menu_id)

        MenuCacheCRUD(self.cache).delete(menu_id=menu_id)

        MenuCacheService(self.cache).invalidate_menus()

        return JSONResponse(status_code=200, content='menu deleted')
