import pickle

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import SUBMENU_LINK, SUBMENUS_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.schemas.submenu import SubMenu as SubMenuSchema
from app.schemas.submenu import SubMenuCreate as SubMenuCreateSchema
from app.schemas.submenu import SubMenuUpdate as SubMenuUpdateSchema
from app.services.database.submenu import SubMenuCRUD, SubMenuService

submenu_router = APIRouter()


@submenu_router.get(
    SUBMENUS_LINK,
    response_model=list[SubMenuSchema],
    tags=['Submenus']
)
def read_submenus(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET operation for retrieving submenus related to a specific menu.
    """
    if all_submenus := cache.get('all_submenus'):
        return pickle.loads(all_submenus)

    result = SubMenuService(db).read_submenus(menu_id=target_menu_id)

    cache.set('all_submenus', pickle.dumps(result))

    return result


@submenu_router.post(
    SUBMENUS_LINK,
    response_model=SubMenuSchema,
    status_code=201,
    tags=['Submenus'],
)
def create_submenu(
    target_menu_id: str,
    submenu: SubMenuCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    POST operation for creating a new submenu for a specific menu.
    """
    result = SubMenuCRUD(db).create_submenu(
        submenu_schema=submenu,
        menu_id=target_menu_id
    )

    cache.set(f'submenu_id_{result.id}', pickle.dumps(result))
    cache.delete(f'menu_id_{target_menu_id}')
    cache.delete('all_submenus')
    cache.delete('all_menus')

    return result


@submenu_router.get(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus']
)
def read_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    GET operation for retrieving a specific submenu of a specific menu.
    """

    if target_submenu := cache.get(f'submenu_id_{target_submenu_id}'):
        return pickle.loads(target_submenu)

    result = SubMenuCRUD(db).read_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

    cache.set(f'submenu_id_{target_submenu_id}', pickle.dumps(result))

    return result


@submenu_router.patch(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus']
)
def update_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    submenu_update: SubMenuUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    PATCH operation for updating a specific submenu of a specific menu.
    """
    result = SubMenuCRUD(db).update_submenu(
        submenu_schema=submenu_update,
        submenu_id=target_submenu_id,
        menu_id=target_menu_id
    )

    cache.set(f'submenu_id_{result.id}', pickle.dumps(result))
    cache.delete(f'menu_id_{target_menu_id}')
    cache.delete('all_submenus')
    cache.delete('all_menus')

    return result


@submenu_router.delete(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus']
)
def delete_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    DELETE operation for deleting a specific submenu of a specific menu.
    """
    result = SubMenuCRUD(db).delete_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

    cache.delete(f'submenu_id_{target_submenu_id}')
    cache.delete(f'menu_id_{target_menu_id}')
    cache.delete('all_submenus')
    cache.delete('all_menus')

    return result
