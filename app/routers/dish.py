from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.base import DISH_LINK, DISHES_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_async_db
from app.models.dish import Dish
from app.schemas.dish import Dish as DishSchema
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema
from app.services.api.dish import DishService

dish_router = APIRouter()


@dish_router.get(
    DISHES_LINK,
    response_model=list[DishSchema],
    tags=['Dishes'],
    summary='Get all dishes'
)
async def get_dishes(
    tasks: BackgroundTasks,
    target_menu_id: str,
    target_submenu_id: str,
    db: AsyncSession = Depends(get_async_db),
    cache: Redis = Depends(redis)
) -> list[Dish]:
    """GET operation for retrieving list of dishes related to a specific submenu."""

    result = await DishService(db, cache, tasks).get_dishes(
        submenu_id=target_submenu_id
    )
    return result


@dish_router.get(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Get specific dish'
)
async def get_dish(
    tasks: BackgroundTasks,
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: AsyncSession = Depends(get_async_db),
    cache: Redis = Depends(redis)
) -> Dish | HTTPException:
    """GET operation for retrieving a specific dish of a specific submenu."""

    result = await DishService(db, cache, tasks).get_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )
    return result


@dish_router.post(
    DISHES_LINK,
    response_model=DishSchema,
    status_code=201,
    tags=['Dishes'],
    summary='Create a dish'
)
async def create_dish(
    tasks: BackgroundTasks,
    target_menu_id: str,
    target_submenu_id: str,
    dish_create_schema: DishCreateSchema,
    db: AsyncSession = Depends(get_async_db),
    cache: Redis = Depends(redis)
) -> Dish:
    """POST operation for creating a new dish under a specific submenu."""

    result = await DishService(db, cache, tasks).create_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_schema=dish_create_schema
    )
    return result


@dish_router.patch(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Update specific dish'
)
async def update_dish(
    tasks: BackgroundTasks,
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    dish_update_schema: DishUpdateSchema,
    db: AsyncSession = Depends(get_async_db),
    cache: Redis = Depends(redis)
) -> Dish | HTTPException:
    """PATCH operation for updating a specific dish of a specific submenu."""

    result = await DishService(db, cache, tasks).update_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id,
        dish_schema=dish_update_schema
    )

    return result


@dish_router.delete(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes'],
    summary='Delete specific dish'
)
async def delete_dish(
    tasks: BackgroundTasks,
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: AsyncSession = Depends(get_async_db),
    cache: Redis = Depends(redis)
) -> JSONResponse:
    """DELETE operation for deleting a specific dish of a specific submenu."""

    result = await DishService(db, cache, tasks).delete_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )

    return result
