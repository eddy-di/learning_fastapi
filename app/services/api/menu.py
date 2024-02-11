from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.menu import Menu
from app.schemas.menu import MenuCreate as MenuCreateSchema
from app.schemas.menu import MenuUpdate as MenuUpdateSchema
from app.services.cache.menu import MenuCacheCRUD
from app.services.database.menu import MenuCRUD
from app.services.main import AppService


class MenuService(AppService):
    """Service for querying the menu data from database and cache."""

    async def get_preview(self) -> list[Menu]:

        if everything := await MenuCacheCRUD(self.cache).get_preview():
            return everything

        result = await MenuCRUD(self.db).get_preview()

        await MenuCacheCRUD(self.cache).set_preview(query_result=result)

        return result

    async def get_menus(self) -> list[Menu] | list[dict]:
        """Query to get list of all menus."""

        if all_menus := await MenuCacheCRUD(self.cache).get_menus():
            return all_menus

        result = await MenuCRUD(self.db).get_menus()

        await MenuCacheCRUD(self.cache).set_menus(query_result=result)

        return result

    async def get_menu(self, menu_id: str) -> Menu:
        """GET operation for specific menu."""
        if target_menu := await MenuCacheCRUD(self.cache).get_menu(menu_id=menu_id):
            return target_menu

        result = await MenuCRUD(self.db).get_menu(menu_id=menu_id)

        await MenuCacheCRUD(self.cache).set_menu(query_result=result)

        return result

    async def create_menu(
        self,
        menu_schema: MenuCreateSchema
    ) -> Menu:
        """POST operation for creating menu."""

        result = await MenuCRUD(self.db).create_menu(menu_schema=menu_schema)

        await MenuCacheCRUD(self.cache).set_menu(query_result=result)

        await MenuCacheCRUD(self.cache).invalidate_menus()

        return result

    async def update_menu(
        self,
        menu_id: str,
        menu_schema: MenuUpdateSchema,
    ) -> Menu | HTTPException:
        """PATCH operation for specific menu."""

        result = await MenuCRUD(self.db).update_menu(
            menu_id=menu_id,
            menu_schema=menu_schema
        )

        await MenuCacheCRUD(self.cache).set_menu(query_result=result)

        await MenuCacheCRUD(self.cache).invalidate_menus()

        return result

    async def delete_menu(
        self,
        menu_id: str,
    ) -> JSONResponse:
        """DELETE operation for specific menu."""

        await MenuCRUD(self.db).delete_menu(menu_id=menu_id)

        await MenuCacheCRUD(self.cache).delete(menu_id=menu_id)

        await MenuCacheCRUD(self.cache).invalidate_menus()

        return JSONResponse(status_code=200, content='menu deleted')
