from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.base import SUBMENU_LINK, SUBMENUS_LINK
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
    db: Session = Depends(get_db)
):
    """
    GET operation for retrieving submenus related to a specific menu.
    """
    result = SubMenuService(db).read_submenus(menu_id=target_menu_id)

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
    db: Session = Depends(get_db)
):
    """
    POST operation for creating a new submenu for a specific menu.
    """
    result = SubMenuCRUD(db).create_submenu(
        submenu_schema=submenu,
        menu_id=target_menu_id
    )

    return result


@submenu_router.get(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus']
)
def read_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db)
):
    """
    GET operation for retrieving a specific submenu of a specific menu.
    """
    result = SubMenuCRUD(db).read_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

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
    db: Session = Depends(get_db)
):
    """
    PATCH operation for updating a specific submenu of a specific menu.
    """
    result = SubMenuCRUD(db).update_submenu(
        submenu_schema=submenu_update,
        submenu_id=target_submenu_id,
        menu_id=target_menu_id
    )
    return result


@submenu_router.delete(
    SUBMENU_LINK,
    response_model=SubMenuSchema,
    tags=['Submenus']
)
def delete_submenu(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db)
):
    """
    DELETE operation for deleting a specific submenu of a specific menu.
    """
    result = SubMenuCRUD(db).delete_submenu(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )
    return result
