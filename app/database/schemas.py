from decimal import Decimal

from pydantic import BaseModel


# dishes schemas
class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: Decimal | None


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None


class Dish(DishBase):
    id: str

    class Config:
        from_attributes = True

# Submenu schemas


class SubMenuBase(BaseModel):
    title: str | None
    description: str | None


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    title: str | None = None
    description: str | None = None


class SubMenu(SubMenuBase):
    id: str
    dishes: list[Dish] = []
    dishes_count: int = 0

    class Config:
        from_attributes = True

# Menu schemas


class MenuBase(BaseModel):
    title: str | None
    description: str | None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str | None = None
    description: str | None = None


class Menu(MenuBase):
    id: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True
