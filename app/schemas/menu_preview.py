from pydantic import BaseModel

from app.schemas.dish import Dish


class SubmenuPreviewBase(BaseModel):
    """SubmenuPreviewBase base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None


class MenuPreviewBase(BaseModel):
    """MenuPreviewBase base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None


class SubmenuPreview(SubmenuPreviewBase):
    """
    SubmenuPreview schema, inherits `SubmenuPreviewBase`\n
    Attributes:
        title: str | None
        description: str | None
        ---completing model with---
        id: str
        dishes: list[Dish] = []
    """

    id: str | None = None
    dishes: list[Dish] = []

    class Config:
        from_attributes = True


class MenuPreview(MenuPreviewBase):
    """
    MenuPreview schema, inherits `MenuPreviewBase`\n
    Attributes:
        title: str | None
        description: str | None
        ---completing model with---
        id: str
        submenus: list[SubmenuPreview] = []
    """

    id: str | None = None
    submenus: list[SubmenuPreview] = []

    class Config:
        from_attributes = True
