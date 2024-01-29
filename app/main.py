from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List
from . import database, models, schemas
from .database import Base, engine


app = FastAPI()

def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# GET endpoint for list of menus, and a count of related items in it
@app.get("/api/v1/menus", response_model=List[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu,
        func.count(distinct(models.SubMenu.id)).label('submenus_count'),
        func.count(distinct(models.Dish.id)).label('dishes_count'),
    )\
        .join(models.SubMenu, models.Menu.id == models.SubMenu.menu_id, isouter=True)\
        .join(models.Dish, models.SubMenu.id == models.Dish.submenu_id, isouter=True)\
        .group_by(models.Menu.id, models.Menu.title, models.Menu.description)\
        .all()
    result = []
    for i in menus:
        menu, submenus_count, dishes_count = i
        result.append({
            "title": menu.title,
            'description': menu.description,
            'id': menu.id,
            'submenus_count': submenus_count,
            'dishes_count': dishes_count
        })
    return result


@app.post('/api/v1/menus', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu 


@app.get("/api/v1/menus/{target_menu_id}", response_model=schemas.Menu)
def read_menu(target_menu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu from the database
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    
    # Check if the menu exists
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    
    db_menu.submenus_count = (
            db.query(func.count(models.SubMenu.id))
            .filter(models.SubMenu.menu_id == db_menu.id)
            .scalar()
        )

    db_menu.dishes_count = (
            db.query(func.count(models.Dish.id))
            .join(models.SubMenu)
            .filter(models.SubMenu.menu_id == db_menu.id)
            .scalar()
        )
    
    return db_menu



@app.patch("/api/v1/menus/{target_menu_id}", response_model=schemas.Menu)
def update_menu(target_menu_id: str, menu_update: schemas.MenuUpdate, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Update menu attributes
    for key, value in menu_update.model_dump(exclude_unset=True).items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)
    return db_menu



@app.delete("/api/v1/menus/{target_menu_id}", response_model=schemas.Menu)
def delete_menu(target_menu_id: str, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    
    # Delete the menu and its associated submenus and dishes
    db.delete(db_menu)
    db.commit()
    return db_menu

# Part for Submenus

# GET operation for retrieving submenus related to a specific menu
@app.get('/api/v1/menus/{target_menu_id}/submenus', response_model=list[schemas.SubMenu])
def get_submenus(target_menu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

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
@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenu, status_code=201)
def create_submenu(target_menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Create the new submenu
    db_submenu = models.SubMenu(**submenu.model_dump(), menu=db_menu)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    return db_submenu


# GET operation for retrieving a specific submenu of a specific menu
@app.get('/api/v1/menus/{target_menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def get_submenu(target_menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    
    db_submenu.dishes_count = (
        db.query(func.count(models.Dish.id))
        .join(models.SubMenu)
        .filter(models.SubMenu.id == db_submenu.id)
        .scalar()
    )

    return db_submenu

# PATCH operation for updating a specific submenu of a specific menu
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def update_submenu(target_menu_id: str, submenu_id: str, submenu_update: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Update submenu attributes
    for key, value in submenu_update.model_dump(exclude_unset=True).items():
        setattr(db_submenu, key, value)

    db.commit()
    db.refresh(db_submenu)
    return db_submenu

# DELETE operation for deleting a specific submenu of a specific menu
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def delete_submenu(target_menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Delete the submenu
    db.delete(db_submenu)
    db.commit()
    return db_submenu

# CRUD for Dishes

# GET operation for retrieving dishes related to a specific submenu
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def get_dishes(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):

    # Fetch the associated dishes
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == target_submenu_id).all()
    
    return dishes

# POST operation for creating a new dish under a specific submenu
@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=schemas.Dish, status_code=201)
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
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.Dish)
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
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.Dish)
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
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.Dish)
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