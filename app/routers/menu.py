import json

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.database import models, schemas
from app.database.database import get_db
from app.database.redis_cache import create_redis as redis

menu_router = APIRouter()


MENUS_LINK = '/api/v1/menus'
MENU_LINK = '/api/v1/menus/{target_menu_id}'


# GET endpoint for list of menus, and a count of related items in it
@menu_router.get(MENUS_LINK, response_model=list[schemas.Menu], tags=['menus'])
def read_menus(db: Session = Depends(get_db), cache: Redis = Depends(redis)):
    if read_menus := cache.get('read_menus'):
        return json.loads(read_menus)
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
            'title': menu.title,
            'description': menu.description,
            'id': menu.id,
            'submenus_count': submenus_count,
            'dishes_count': dishes_count
        })
    cache.set('read_menus', json.dumps(result))
    # print(type(cache.get('read_menus')))
    # print(type(json.loads(cache.get('read_menus'))))
    # print(type(result))
    return result


@menu_router.post(MENUS_LINK, response_model=schemas.Menu, status_code=201, tags=['menus'])
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@menu_router.get(MENU_LINK, response_model=schemas.Menu, tags=['menus'])
def read_menu(target_menu_id: str, db: Session = Depends(get_db)):
    # Fetch the menu from the database
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    # Check if the menu exists
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

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


@menu_router.patch(MENU_LINK, response_model=schemas.Menu, tags=['menus'])
def update_menu(target_menu_id: str, menu_update: schemas.MenuUpdate, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Update menu attributes
    for key, value in menu_update.model_dump(exclude_unset=True).items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)
    return db_menu


@menu_router.delete(MENU_LINK, response_model=schemas.Menu, tags=['menus'])
def delete_menu(target_menu_id: str, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Delete the menu and its associated submenus and dishes
    db.delete(db_menu)
    db.commit()
    return db_menu
