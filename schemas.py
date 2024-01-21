from decimal import Decimal
from pydantic import BaseModel

# dishes schemas
class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: str

    class Config:
        from_attributes = True

# Submenu schemas
class SubMenuBase(BaseModel):
    title: str
    description: str

class SubMenuCreate(SubMenuBase):
    pass

class SubMenu(SubMenuBase):
    id: str
    dishes: list[Dish] = []

    class Config:
        from_attributes = True

# Menu schemas
class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: str
    submenus: list[SubMenu] = []

    class Config:
        from_attributes = True

# for counts
class SubMenuWithCounts(SubMenu):
    dish_count: int

class MenuWithCounts(Menu):
    submenu_count: int
    dish_count: int
