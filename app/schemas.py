from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

# dishes schemas
class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal

class DishCreate(DishBase):
    pass

class DishUpdate(DishBase):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None

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

class SubMenuUpdate(SubMenuBase):
    title: Optional[str] = None
    description: Optional[str] = None

class SubMenu(SubMenuBase):
    id: str
    dishes: list[Dish] = []
    dishes_count: int | None = None

    class Config:
        from_attributes = True

# Menu schemas
class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    title: Optional[str] = None
    description: Optional[str] = None

class Menu(MenuBase):
    id: str
    submenus_count: int | None = None
    dishes_count: int | None = None

    class Config:
        from_attributes = True
