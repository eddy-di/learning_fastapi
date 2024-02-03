from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.base import DISH_LINK, DISHES_LINK
from app.config.database import get_db
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.schemas.dish import Dish as DishSchema
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema

dish_router = APIRouter()


# GET operation for retrieving dishes related to a specific submenu


@dish_router.get(DISHES_LINK, response_model=list[DishSchema], tags=['Dishes'])
def get_dishes(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):

    # Fetch the associated dishes
    dishes = db.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()

    return dishes

# POST operation for creating a new dish under a specific submenu


@dish_router.post(DISHES_LINK, response_model=DishSchema, status_code=201, tags=['Dishes'])
def create_dish(target_menu_id: str, target_submenu_id: str, dish: DishCreateSchema, db: Session = Depends(get_db)):

    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the submenu to check if it exists
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Create the new dish
    db_dish = Dish(**dish.model_dump(), submenu=db_submenu)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    return db_dish


# GET operation for retrieving a specific dish of a specific submenu
@dish_router.get(DISH_LINK, response_model=DishSchema, tags=['Dishes'])
def get_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)):

    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the submenu to check if it exists
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Fetch the specific dish
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id,
                                    Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish


# PATCH operation for updating a specific dish of a specific submenu
@dish_router.patch(DISH_LINK, response_model=DishSchema, tags=['Dishes'])
def update_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, dish_update: DishUpdateSchema, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the submenu to check if it exists
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Fetch the specific dish
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id,
                                    Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')

    # Update dish attributes
    for key, value in dish_update.model_dump(exclude_unset=True).items():
        setattr(db_dish, key, value)

    db.commit()
    db.refresh(db_dish)
    return db_dish

# DELETE operation for deleting a specific dish of a specific submenu


@dish_router.delete(DISH_LINK, response_model=DishSchema, tags=['Dishes'])
def delete_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Fetch the submenu to check if it exists
    db_submenu = db.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                          SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Fetch the specific dish
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id,
                                    Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')

    # Delete the dish
    db.delete(db_dish)
    db.commit()
    return db_dish
