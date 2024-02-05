from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import SUBMENU_LINK, SUBMENUS_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenu as SubMenuSchema
from app.schemas.submenu import SubMenuCreate as SubMenuCreateSchema
from app.schemas.submenu import SubMenuUpdate as SubMenuUpdateSchema
from app.services.api.submenu import SubMenuService

submenu_router = APIRouter()


@submenu_router.get(
    SUBMENUS_LINK,
    response_model=list[SubMenuSchema],
    tags=['Submenus'],
    summary='Get all submenus'
)
def get_submenus(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> list[SubMenu] | list[dict]:
    """GET operation for retrieving submenus related to a specific menu."""
    result = SubMenuService(db, cache).get_submenus(menu_id=target_menu_id)
    return result


@submenu_router.get(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus'],
    summary='Get specific submenu'
)
def get_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> SubMenu | HTTPException:
    """GET operation for retrieving a specific submenu of a specific menu."""

    result = SubMenuService(db, cache).get_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

    return result


@submenu_router.post(
    SUBMENUS_LINK,
    response_model=SubMenuSchema,
    status_code=201,
    tags=['Submenus'],
    summary='Create a submenu'
)
def create_submenu(
    target_menu_id: str,
    submenu_create_schema: SubMenuCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> SubMenu | HTTPException:
    """POST operation for creating a new submenu for a specific menu."""

    result = SubMenuService(db, cache).create_submenu(
        menu_id=target_menu_id,
        submenu_schema=submenu_create_schema
    )

    return result


@submenu_router.patch(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus'],
    summary='Update specific submenu'
)
def update_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    submenu_update_schema: SubMenuUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> SubMenu | HTTPException:
    """PATCH operation for updating a specific submenu of a specific menu."""

    result = SubMenuService(db, cache).update_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        submenu_schema=submenu_update_schema,
    )

    return result


@submenu_router.delete(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus'],
    summary='Delete specific submenu'
)
def delete_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
) -> JSONResponse:
    """DELETE operation for deleting a specific submenu of a specific menu."""

    result = SubMenuService(db, cache).delete_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

    return result
