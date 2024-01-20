from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import database, models, schemas


app = FastAPI()



def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


# db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/api/v1/menus', response_model=schemas.Menu)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@app.get("/api/v1/menus/{target_menu_id}", response_model=schemas.Menu)
def read_menu(target_menu_id: str, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu


@app.get("/api/v1/menus/", response_model=List[schemas.Menu])
def read_menus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    menus = db.query(models.Menu).offset(skip).limit(limit).all()
    return menus


@app.get("/api/v1/menus/{target_menu_id}/submenu-count", response_model=int)
def get_submenu_count(target_menu_id: str, db: Session = Depends(get_db)):
    submenu_count = (
        db.query(func.count(models.SubMenu.id))
        .filter(models.SubMenu.menu_id == target_menu_id)
        .scalar()
    )
    return submenu_count

@app.get("/api/v1/menus/{submenu_id}/dish-count", response_model=int)
def get_dish_count(submenu_id: str, db: Session = Depends(get_db)):
    dish_count = (
        db.query(func.count(models.Dish.id))
        .filter(models.Dish.submenu_id == submenu_id)
        .scalar()
    )
    return dish_count