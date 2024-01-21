from decimal import Decimal
from pydantic import BaseModel

class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: str

    class Config:
        from_attributes = True

class SubMenuBase(BaseModel):
    title: str
    description: str

class SubMenuCreate(SubMenuBase):
    # menu_id: str
    ...

class SubMenu(SubMenuCreate):
    id: str
    menu: Menu

    class Config:
        from_attributes = True

class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal

class DishCreate(DishBase):
    # submenu_id: str
    title: str
    description: str
    price: Decimal
    submenu: SubMenu

class Dish(DishBase):
    id: str
    submenu: SubMenu

    class Config:
        from_attributes = True

class SubMenuWithCounts(SubMenu):
    dish_count: int

class MenuWithCounts(Menu):
    submenu_count: int
    dish_count: int
