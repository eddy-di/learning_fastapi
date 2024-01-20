from pydantic import BaseModel
from typing import List

class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: str

    class Config:
        orm_mode = True

class SubMenuBase(BaseModel):
    title: str
    description: str

class SubMenuCreate(SubMenuBase):
    menu_id: str

class SubMenu(SubMenuBase):
    id: str
    menu: Menu

    class Config:
        orm_mode = True

class DishBase(BaseModel):
    title: str
    description: str
    price: float

class DishCreate(DishBase):
    submenu_id: str

class Dish(DishBase):
    id: str
    submenu: SubMenu

    class Config:
        orm_mode = True
