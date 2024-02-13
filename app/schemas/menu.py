from pydantic import BaseModel

from .submenu import SubMenu


class MenuBase(BaseModel):
    """Menus base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None


class MenuCreate(MenuBase):
    """
    Menu create schema, inherits `MenuBase`\n
    Attributes:
        title: str | None
        description: str | None
        --adding to the model---
        id: str | None
    """

    id: str | None


class MenuUpdate(MenuBase):
    """
    Menu update schema, inherits `MenuBase`\n
    Attributes:
        title: str | None
        description: str | None
    """

    title: str | None = None
    description: str | None = None


class Menu(MenuBase):
    """
    Menu schema, inherits `MenuBase`\n
    Attributes:
        title: str | None
        description: str | None
        ---adding to the model---
        id: str | None
        submenus: list[SubMenu] = []
        submenus_count: int = 0
        dishes_count: int = 0
    """

    id: str
    submenus: list[SubMenu] = []
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True
