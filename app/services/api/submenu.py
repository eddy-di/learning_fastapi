from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenuCreate as SubMenuCreateSchema
from app.schemas.submenu import SubMenuUpdate as SubMenuUpdateSchema
from app.services.cache.submenu import SubMenuCacheCRUD
from app.services.database.submenu import SubMenuCRUD
from app.services.main import AppService


class SubMenuService(AppService):
    """Service for querying the submenu data from database and cache."""

    def get_submenus(self, menu_id: str) -> list[SubMenu] | list[dict]:
        """Query to get list of all submenus."""

        if all_submenus := SubMenuCacheCRUD(self.cache).get_submenus():
            return all_submenus

        result = SubMenuCRUD(self.db).get_submenus(menu_id=menu_id)

        SubMenuCacheCRUD(self.cache).set_submenus(query_result=result)

        return result

    def get_submenu(
        self,
        menu_id: str,
        submenu_id: str,
    ) -> SubMenu | HTTPException:
        """GET operation for retrieving a specific submenu of a specific menu."""

        if target_submenu := SubMenuCacheCRUD(self.cache).get_submenu(submenu_id=submenu_id):
            return target_submenu

        result = SubMenuCRUD(self.db).get_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id
        )

        SubMenuCacheCRUD(self.cache).set_submenu(query_result=result)

        return result

    def create_submenu(
        self,
        menu_id: str,
        submenu_schema: SubMenuCreateSchema,
    ) -> SubMenu | HTTPException:
        """POST operation for creating a new submenu for a specific menu."""

        result = SubMenuCRUD(self.db).create_submenu(
            menu_id=menu_id,
            submenu_schema=submenu_schema,
        )

        SubMenuCacheCRUD(self.cache).set_submenu(query_result=result)

        SubMenuCacheCRUD(self.cache).invalidate_submenus(menu_id=menu_id)

        return result

    def update_submenu(
        self,
        menu_id: str,
        submenu_id: str,
        submenu_schema: SubMenuUpdateSchema,
    ) -> SubMenu | HTTPException:
        """PATCH operation for updating a specific submenu of a specific menu."""

        result = SubMenuCRUD(self.db).update_submenu(
            submenu_schema=submenu_schema,
            submenu_id=submenu_id,
            menu_id=menu_id
        )

        SubMenuCacheCRUD(self.cache).set_submenu(query_result=result)
        SubMenuCacheCRUD(self.cache).invalidate_submenus(menu_id=menu_id)

        return result

    def delete_submenu(
        self,
        menu_id: str,
        submenu_id: str,
    ) -> JSONResponse:
        """DELETE operation for deleting a specific submenu of a specific menu."""

        SubMenuCRUD(self.db).delete_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id
        )

        SubMenuCacheCRUD(self.cache).delete(submenu_id=submenu_id)

        SubMenuCacheCRUD(self.cache).invalidate_submenus(menu_id=menu_id)

        return JSONResponse(status_code=200, content='submenu deleted')
