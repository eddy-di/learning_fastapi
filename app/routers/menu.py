from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import MENU_LINK, MENUS_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.models.menu import Menu
from app.schemas.menu import Menu as MenuSchema
from app.schemas.menu import MenuCreate as MenuCreateSchema
from app.schemas.menu import MenuUpdate as MenuUpdateSchema
from app.services.api.menu import MenuService

menu_router = APIRouter()


@menu_router.get(
    MENUS_LINK,
    response_model=list[MenuSchema],
    tags=['Menus'],
    summary='Get all menus'
)
def get_menus(
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> list[Menu] | list[dict]:
    """GET endpoint for list of menus, and a count of related items in it."""
    result = MenuService(db, cache).get_menus()
    return result


@menu_router.get(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Get specific menu'
)
def get_menu(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> Menu | HTTPException:
    """GET operation for specific menu"""

    result = MenuService(db, cache).get_menu(menu_id=target_menu_id)
    return result


@menu_router.post(
    MENUS_LINK,
    response_model=MenuSchema,
    status_code=201,
    tags=['Menus'],
    summary='Create a menu'
)
def create_menu(
    menu_create_schema: MenuCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> Menu:
    """POST operation for creating menu."""

    result = MenuService(db, cache).create_menu(menu_schema=menu_create_schema)
    return result


@menu_router.patch(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Update specific menu'
)
def update_menu(
    target_menu_id: str,
    menu_update_schema: MenuUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> Menu | HTTPException:
    """PATCH operation for specific menu."""

    result = MenuService(db, cache).update_menu(
        menu_id=target_menu_id,
        menu_schema=menu_update_schema
    )
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
) -> JSONResponse:
    """DELETE operation for specific menu."""

    result = MenuService(db, cache).delete_menu(menu_id=target_menu_id)
    return result
