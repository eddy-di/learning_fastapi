from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import database, models, schemas
from fastapi.responses import JSONResponse


app = FastAPI()

def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()



# GET endpoint for list of menus, and a count of related items in it
@app.get("/api/v1/menus", response_model=List[schemas.MenuWithCounts])
def read_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()

    # Fetch submenu count for each menu
    for menu in menus:
        menu.submenu_count = (
            db.query(func.count(models.SubMenu.id))
            .filter(models.SubMenu.menu_id == menu.id)
            .scalar()
        )

        menu.dish_count = (
            db.query(func.count(models.Dish.id))
            .join(models.SubMenu)
            .filter(models.SubMenu.menu_id == menu.id)
            .scalar()
        )

    return menus



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
    
    return db_menu



@app.patch("/api/v1/menus/{target_menu_id}", response_model=schemas.Menu)
def update_menu(target_menu_id: str, menu_update: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Update menu attributes
    for key, value in menu_update.dict().items():
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
    
    return submenus


# POST operation for creating a new submenu for a specific menu
@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenu, status_code=201)
def create_submenu(target_menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    print(db_menu)
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

    return db_submenu

# PATCH operation for updating a specific submenu of a specific menu
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def update_submenu(target_menu_id: str, submenu_id: str, submenu_update: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    # Fetch the menu first to check if it exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # Fetch the specific submenu
    db_submenu = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id, models.SubMenu.menu_id == target_menu_id).first()

    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Update submenu attributes
    for key, value in submenu_update.model_dump().items():
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