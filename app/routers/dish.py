from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import DISH_LINK, DISHES_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.schemas.dish import Dish as DishSchema
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema
from app.services.cache.dish import DishCacheCRUD, DishCacheService
from app.services.database.dish import DishCRUD, DishService

dish_router = APIRouter()


@dish_router.get(
    DISHES_LINK,
    response_model=list[DishSchema],
    tags=['Dishes'],
    summary='Get all dishes'
)
def read_dishes(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET operation for retrieving list of dishes related to a specific submenu
    """

    if all_dishes := DishCacheService(cache).read_dishes():
        return all_dishes

    result = DishService(db).read_dishes(
        submenu_id=target_submenu_id
    )

    DishCacheService(cache).set_dishes(query_result=result)

    return result


@dish_router.post(
    DISHES_LINK,
    response_model=DishSchema,
    status_code=201,
    tags=['Dishes'],
    summary='Create a dish'
)
def create_dish(
    target_menu_id: str,
    target_submenu_id: str,
    dish: DishCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    POST operation for creating a new dish under a specific submenu
    """

    result = DishCRUD(db).create_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_schema=dish
    )

    DishCacheCRUD(cache).set_dish(query_result=result)

    DishCacheService(cache).invalidate_dishes(menu_id=target_menu_id, submenu_id=target_submenu_id)

    return result


@dish_router.get(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Get specific dish'
)
def read_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET operation for retrieving a specific dish of a specific submenu
    """

    if target_dish := DishCacheCRUD(cache).read_dish(dish_id=target_dish_id):
        return target_dish

    result = DishCRUD(db).read_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )

    DishCacheCRUD(cache).set_dish(query_result=result)

    return result


@dish_router.patch(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Update specific dish'
)
def update_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    dish_update: DishUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    PATCH operation for updating a specific dish of a specific submenu
    """

    result = DishCRUD(db).update_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id,
        dish_schema=dish_update
    )

    DishCacheCRUD(cache).set_dish(query_result=result)

    DishCacheService(cache).invalidate_dishes(menu_id=target_menu_id, submenu_id=target_submenu_id)

    return result


@dish_router.delete(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Delete specific dish'
)
def delete_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    DELETE operation for deleting a specific dish of a specific submenu
    """

    DishCRUD(db).delete_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )

    DishCacheCRUD(cache).delete(dish_id=target_dish_id)

    DishCacheService(cache).invalidate_dishes(menu_id=target_menu_id, submenu_id=target_submenu_id)

    return JSONResponse(status_code=200, content='dish deleted')
