from pydantic import BaseModel


class SubMenuBase(BaseModel):
    """SubMenu base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None


class SubMenuCreate(SubMenuBase):
    """
    SubMenu create schema, inherits `SubMenuBase`\n
    Attributes:
        title: str | None
        description: str | None
        ---adding to the model---
        id: str | None
    """

    id: str | None = None


class SubMenuUpdate(SubMenuBase):
    """
    SubMenu update schema, inherits `SubMenuBase`\n
    Attributes:
        title: str | None
        description: str | None
    """

    title: str | None = None
    description: str | None = None


class SubMenu(SubMenuBase):
    """
    SubMenu schema, inherits `SubMenuBase`\n
    Attributes:
        title: str | None
        description: str | None
        ---adding to the model---
        id: str | None
        dishes_count: int = 0
    """

    id: str
    dishes_count: int = 0

    class Config:
        from_attributes = True
