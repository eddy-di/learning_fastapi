from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.dish import Dish
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema
from app.services.cache.dish import DishCacheCRUD
from app.services.database.dish import DishCRUD
from app.services.main import AppService


class DishService(AppService):
    """Service for querying the dish data from database and cache."""

    async def get_dishes(
        self,
        submenu_id: str,
    ) -> list[Dish]:
        """GET operation for retrieving list of dishes related to a specific submenu."""

        if all_dishes := await DishCacheCRUD(self.cache).get_dishes():
            return all_dishes

        result = await DishCRUD(self.db).get_dishes(
            submenu_id=submenu_id
        )
        self.tasks.add_task(DishCacheCRUD(self.cache).set_dishes, result)
        # await DishCacheCRUD(self.cache).set_dishes(query_result=result)

        return result

    async def get_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
    ) -> Dish | HTTPException:
        """GET operation for retrieving a specific dish of a specific submenu."""

        if target_dish := await DishCacheCRUD(self.cache).get_dish(dish_id=dish_id):
            return target_dish

        result = await DishCRUD(self.db).get_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )
        self.tasks.add_task(DishCacheCRUD(self.cache).set_dish, result)

        # await DishCacheCRUD(self.cache).set_dish(query_result=result)

        return result

    async def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_schema: DishCreateSchema,
    ) -> Dish:
        """POST operation for creating a new dish under a specific submenu."""

        result = await DishCRUD(self.db).create_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_schema=dish_schema
        )
        self.tasks.add_task(DishCacheCRUD(self.cache).set_dish, result)
        self.tasks.add_task(DishCacheCRUD(self.cache).invalidate_dishes, menu_id, submenu_id)
        # await DishCacheCRUD(self.cache).set_dish(query_result=result)
        # await DishCacheCRUD(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return result

    async def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_schema: DishUpdateSchema,
    ) -> Dish | HTTPException:
        """PATCH operation for updating a specific dish of a specific submenu."""

        result = await DishCRUD(self.db).update_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            dish_schema=dish_schema
        )
        self.tasks.add_task(DishCacheCRUD(self.cache).set_dish, result)
        self.tasks.add_task(DishCacheCRUD(self.cache).invalidate_dishes, menu_id, submenu_id)
        # await DishCacheCRUD(self.cache).set_dish(query_result=result)
        # await DishCacheCRUD(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return result

    async def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,

    ) -> JSONResponse:
        """DELETE operation for deleting a specific dish of a specific submenu."""

        await DishCRUD(self.db).delete_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        )
        self.tasks.add_task(DishCacheCRUD(self.cache).delete, dish_id)
        self.tasks.add_task(DishCacheCRUD(self.cache).invalidate_dishes, menu_id, submenu_id)
        # await DishCacheCRUD(self.cache).delete(dish_id=dish_id)
        # await DishCacheCRUD(self.cache).invalidate_dishes(menu_id=menu_id, submenu_id=submenu_id)

        return JSONResponse(status_code=200, content='dish deleted')
