from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.dish import Dish as DishModel
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema
from app.services.cache.dish import DishCacheCRUD, DishCacheService
from app.services.database.dish import DishCRUD
from app.services.main import AppService


class DishService(AppService):
    """Service for querying the list of all dishes."""

    def get_dishes(
        self,
        menu_id: str,
        submenu_id: str,
    ) -> list[DishModel]:
        """GET operation for retrieving list of dishes related to a specific submenu"""

        if all_dishes := DishCacheService(self.cache).get_dishes():
            return all_dishes

        result = DishCRUD(self.db).get_dishes(
            submenu_id=submenu_id
        )

        DishCacheService(self.cache).set_dishes(query_result=result)

        return result

    def get_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
    ) -> DishModel | HTTPException:
        """GET operation for retrieving a specific dish of a specific submenu"""

        if target_dish := DishCacheCRUD(self.cache).get_dish(dish_id=dish_id):
            return target_dish

        result = DishCRUD(self.db).get_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )

        DishCacheCRUD(self.cache).set_dish(query_result=result)

        return result

    def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_schema: DishCreateSchema,
    ) -> DishModel:
        """POST operation for creating a new dish under a specific submenu"""

        result = DishCRUD(self.db).create_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_schema=dish_schema
        )

        DishCacheCRUD(self.cache).set_dish(query_result=result)

        DishCacheService(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return result

    def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_schema: DishUpdateSchema,
    ) -> DishModel | HTTPException:
        """PATCH operation for updating a specific dish of a specific submenu"""

        result = DishCRUD(self.db).update_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            dish_schema=dish_schema
        )

        DishCacheCRUD(self.cache).set_dish(query_result=result)

        DishCacheService(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return result

    def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,

    ) -> JSONResponse:
        """DELETE operation for deleting a specific dish of a specific submenu"""

        DishCRUD(self.db).delete_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )

        DishCacheCRUD(self.cache).delete(dish_id=dish_id)

        DishCacheService(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return JSONResponse(status_code=200, content='dish deleted')
