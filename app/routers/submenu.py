from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import models, schemas
from app.database.database import get_db

submenu_router = APIRouter()


SUBMENUS_LINK = '/api/v1/menus/{target_menu_id}/submenus'
SUBMENU_LINK = '/api/v1/menus/{target_menu_id}/submenus/{submenu_id}'


# GET operation for retrieving submenus related to a specific menu
@submenu_router.get(SUBMENUS_LINK, response_model=list[schemas.SubMenu], tags=['submenus'])
def get_submenus(target_menu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the associated submenus
    submenus = db.query(models.SubMenu).filter(models.SubMenu.menu_id == target_menu_id).all()

    for submenu in submenus:
        submenu.dishes_count = (
            db.query(func.count(models.Dish.id))
            .join(models.SubMenu)
            .filter(models.SubMenu.menu_id == target_menu_id)
            .scalar()
        )

    return submenus


# POST operation for creating a new submenu for a specific menu
@submenu_router.post(SUBMENUS_LINK, response_model=schemas.SubMenu, status_code=201, tags=['submenus'])
def create_submenu(target_menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Create the new submenu
    db_submenu = models.SubMenu(**submenu.model_dump(), menu=db_menu)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    return db_submenu


# GET operation for retrieving a specific submenu of a specific menu
@submenu_router.get(SUBMENU_LINK, response_model=schemas.SubMenu, tags=['submenus'])
def get_submenu(target_menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id,
                                                 models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    db_submenu.dishes_count = (
        db.query(func.count(models.Dish.id))
        .join(models.SubMenu)
        .filter(models.SubMenu.id == db_submenu.id)
        .scalar()
    )

    return db_submenu

# PATCH operation for updating a specific submenu of a specific menu


@submenu_router.patch(SUBMENU_LINK, response_model=schemas.SubMenu, tags=['submenus'])
def update_submenu(target_menu_id: str, submenu_id: str, submenu_update: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id,
                                                 models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Update submenu attributes
    for key, value in submenu_update.model_dump(exclude_unset=True).items():
        setattr(db_submenu, key, value)

    db.commit()
    db.refresh(db_submenu)
    return db_submenu

# DELETE operation for deleting a specific submenu of a specific menu


@submenu_router.delete(SUBMENU_LINK, response_model=schemas.SubMenu, tags=['submenus'])
def delete_submenu(target_menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id,
                                                 models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Delete the submenu
    db.delete(db_submenu)
    db.commit()
    return db_submenu
