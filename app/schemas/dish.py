from decimal import Decimal

from pydantic import BaseModel


class DishBase(BaseModel):

    """Dish base schema, inherits `BaseModel` from `pydantic`"""

    title: str | None
    description: str | None
    price: Decimal | None


class DishCreate(DishBase):

    """Dish create schema, iherits `DishBase`"""

    pass


class DishUpdate(DishBase):

    """Dish update schema, inherits `DishBase`"""

    title: str | None = None
    description: str | None = None
    price: Decimal | None = None


class Dish(DishBase):

    """Dish schema, iherits `DishBase`"""

    id: str

    class Config:
        from_attributes = True
