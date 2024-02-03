import json

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.config.base import MENU_LINK, MENUS_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.schemas.menu import Menu as MenuSchema
from app.schemas.menu import MenuCreate as MenuCreateSchema
from app.schemas.menu import MenuUpdate as MenuUpdateSchema

menu_router = APIRouter()


# GET endpoint for list of menus, and a count of related items in it
@menu_router.get(
    MENUS_LINK,
    response_model=list[MenuSchema],
    tags=['Menus'],
    summary='Get all menus'
)
def read_menus(
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    """
    Endoint for getting list of menus.
    """
    if read_menus := cache.get('read_menus'):
        return json.loads(read_menus)
    menus = db.query(Menu,
                     func.count(distinct(SubMenu.id)).label('submenus_count'),
                     func.count(distinct(Dish.id)).label('dishes_count'),
                     )\
        .join(SubMenu, Menu.id == SubMenu.menu_id, isouter=True)\
        .join(Dish, SubMenu.id == Dish.submenu_id, isouter=True)\
        .group_by(Menu.id, Menu.title, Menu.description)\
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


@menu_router.post(
    MENUS_LINK,
    response_model=MenuSchema,
    status_code=201,
    tags=['Menus'],
    summary='Create a menu'
)
def create_menu(
    menu: MenuCreateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@menu_router.get(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Get specific menu'
)
def read_menu(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    # Fetch the menu from the database
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    # Check if the menu exists
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    db_menu.submenus_count = (
        db.query(func.count(SubMenu.id))
        .filter(SubMenu.menu_id == db_menu.id)
        .scalar()
    )

    db_menu.dishes_count = (
        db.query(func.count(Dish.id))
        .join(SubMenu)
        .filter(SubMenu.menu_id == db_menu.id)
        .scalar()
    )

    return db_menu


@menu_router.patch(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Update specific menu'
)
def update_menu(
    target_menu_id: str,
    menu_update: MenuUpdateSchema,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Update menu attributes
    for key, value in menu_update.model_dump(exclude_unset=True).items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)
    return db_menu


@menu_router.delete(
    MENU_LINK,
    response_model=MenuSchema,
    tags=['Menus'],
    summary='Delete specific menu',
)
def delete_menu(
    target_menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()

    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    # Delete the menu and its associated submenus and dishes
    db.delete(db_menu)
    db.commit()
    return db_menu
