from pydantic import BaseModel

from .submenu import SubMenu


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
    submenus: list[SubMenu] = []
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True
