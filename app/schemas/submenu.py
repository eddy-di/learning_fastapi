from pydantic import BaseModel

from .dish import Dish


class SubMenuBase(BaseModel):

    """SubMenu base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None


class SubMenuCreate(SubMenuBase):

    """SubMenu create schema, inherits `SubMenuBase`"""

    pass


class SubMenuUpdate(SubMenuBase):

    """SubMenu update schema, inherits `SubMenuBase`"""

    title: str | None = None
    description: str | None = None


class SubMenu(SubMenuBase):

    """SubMenu schema, inherits `SubMenuBase`"""

    id: str
    dishes: list[Dish] = []
    dishes_count: int = 0

    class Config:
        from_attributes = True
