from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import MENU_LINK, MENUS_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.schemas.menu import Menu as MenuSchema
from app.schemas.menu import MenuCreate as MenuCreateSchema
from app.schemas.menu import MenuUpdate as MenuUpdateSchema
from app.services.cache.menu import MenuCacheCRUD, MenuCacheService
from app.services.database.menu import MenuCRUD, MenuService

menu_router = APIRouter()


@menu_router.get(
    MENUS_LINK,
    response_model=list[MenuSchema],
    tags=['Menus'],
    summary='Get all menus'
)
def read_menus(
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET endpoint for list of menus, and a count of related items in it
    """

    MenuCacheService(cache).read_menus()

    result = MenuService(db).read_menus()

    MenuCacheService(cache).set_menus(query_result=result)

    return result


@menu_router.post(
    MENUS_LINK,
    response_model=MenuSchema,
    status_code=201,
    tags=['Menus'],
    summary='Create a menu'
)
def create_menu(
    menu: MenuCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    POST operation for creating menu.
    """

    result = MenuCRUD(db).create_menu(menu_schema=menu)

    MenuCacheCRUD(cache).create_or_update(query_result=result)

    MenuCacheService(cache).invalidate_menus()

    return result


@menu_router.get(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Get specific menu'
)
def read_menu(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET operation for specific menu.
    """

    MenuCacheCRUD(cache).read_menu(menu_id=target_menu_id)

    result = MenuCRUD(db).read_menu(menu_id=target_menu_id)

    MenuCacheCRUD(cache).set_menu(menu_id=target_menu_id, query_result=result)

    return result


@menu_router.patch(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Update specific menu'
)
def update_menu(
    target_menu_id: str,
    menu_update: MenuUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    PATCH operation for specific menu.
    """

    result = MenuCRUD(db).update_menu(
        menu_id=target_menu_id,
        menu_schema=menu_update
    )

    MenuCacheCRUD(cache).create_or_update(query_result=result)

    MenuCacheService(cache).invalidate_menus()

    return result


@menu_router.delete(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Delete specific menu',
)
def delete_menu(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    DELETE operation for specific menu.
    """

    result = MenuCRUD(db).delete_menu(menu_id=target_menu_id)

    MenuCacheCRUD(cache).delete(menu_id=target_menu_id)

    MenuCacheService(cache).invalidate_menus()

    return result
