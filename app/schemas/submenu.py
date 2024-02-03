from pydantic import BaseModel

from .dish import Dish


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
