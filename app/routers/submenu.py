from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config.base import SUBMENU_LINK, SUBMENUS_LINK
from app.config.database import get_db
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenu as SubMenuSchema
from app.schemas.submenu import SubMenuCreate as SubMenuCreateSchema
from app.schemas.submenu import SubMenuUpdate as SubMenuUpdateSchema

submenu_router = APIRouter()


# GET operation for retrieving submenus related to a specific menu
@submenu_router.get(SUBMENUS_LINK, response_model=list[SubMenuSchema], tags=['Submenus'])
def get_submenus(target_menu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the associated submenus
    submenus = db.query(SubMenu).filter(SubMenu.menu_id == target_menu_id).all()

    for submenu in submenus:
        submenu.dishes_count = (
            db.query(func.count(Dish.id))
            .join(SubMenu)
            .filter(SubMenu.menu_id == target_menu_id)
            .scalar()
        )

    return submenus


# POST operation for creating a new submenu for a specific menu
@submenu_router.post(SUBMENUS_LINK, response_model=SubMenuSchema, status_code=201, tags=['Submenus'])
def create_submenu(target_menu_id: str, submenu: SubMenuCreateSchema, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Create the new submenu
    db_submenu = SubMenu(**submenu.model_dump(), menu=db_menu)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    return db_submenu


# GET operation for retrieving a specific submenu of a specific menu
@submenu_router.get(SUBMENU_LINK, response_model=SubMenuSchema, tags=['Submenus'])
def get_submenu(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    db_submenu.dishes_count = (
        db.query(func.count(Dish.id))
        .join(SubMenu)
        .filter(SubMenu.id == db_submenu.id)
        .scalar()
    )

    return db_submenu

# PATCH operation for updating a specific submenu of a specific menu


@submenu_router.patch(SUBMENU_LINK, response_model=SubMenuSchema, tags=['Submenus'])
def update_submenu(target_menu_id: str, target_submenu_id: str, submenu_update: SubMenuUpdateSchema, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Update submenu attributes
    for key, value in submenu_update.model_dump(exclude_unset=True).items():
        setattr(db_submenu, key, value)

    db.commit()
    db.refresh(db_submenu)
    return db_submenu

# DELETE operation for deleting a specific submenu of a specific menu


@submenu_router.delete(SUBMENU_LINK, response_model=SubMenuSchema, tags=['Submenus'])
def delete_submenu(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Delete the submenu
    db.delete(db_submenu)
    db.commit()
    return db_submenu
