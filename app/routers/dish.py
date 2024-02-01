from fastapi import APIRouter
from app.database import models, schemas
from app.database.database import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

dish_router = APIRouter()

DISHES_LINK = "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes"
DISH_LINK = "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}"

# GET operation for retrieving dishes related to a specific submenu
@dish_router.get(DISHES_LINK, response_model=List[schemas.Dish], tags=['dishes'])
def get_dishes(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):


    # Fetch the associated dishes
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == target_submenu_id).all()
    
    return dishes

# POST operation for creating a new dish under a specific submenu
@dish_router.post(DISHES_LINK, response_model=schemas.Dish, status_code=201, tags=['dishes'])
def create_dish(target_menu_id: str, target_submenu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)):

    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the submenu to check if it exists
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == target_submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Create the new dish
    db_dish = models.Dish(**dish.model_dump(), submenu=db_submenu)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    return db_dish


# GET operation for retrieving a specific dish of a specific submenu
@dish_router.get(DISH_LINK, response_model=schemas.Dish, tags=['dishes'])
def get_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)):

    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the submenu to check if it exists
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == target_submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Fetch the specific dish
    db_dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return db_dish


# PATCH operation for updating a specific dish of a specific submenu
@dish_router.patch(DISH_LINK, response_model=schemas.Dish, tags=['dishes'])
def update_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, dish_update: schemas.DishUpdate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the submenu to check if it exists
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == target_submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Fetch the specific dish
    db_dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    # Update dish attributes
    for key, value in dish_update.model_dump(exclude_unset=True).items():
        setattr(db_dish, key, value)

    db.commit()
    db.refresh(db_dish)
    return db_dish

# DELETE operation for deleting a specific dish of a specific submenu
@dish_router.delete(DISH_LINK, response_model=schemas.Dish, tags=['dishes'])
def delete_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the submenu to check if it exists
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == target_submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Fetch the specific dish
    db_dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()

    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    # Delete the dish
    db.delete(db_dish)
    db.commit()
    return db_dish