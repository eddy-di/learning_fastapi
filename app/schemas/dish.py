from decimal import Decimal

from pydantic import BaseModel, Field


class DishBase(BaseModel):
    """
    Dish base schema, inherits `BaseModel` from `pydantic`\n
    Attributes:
        title: str | None
        description: str | None
        price: Decimal | None
        discount: int | 0
    """

    title: str | None
    description: str | None
    price: Decimal | None
    discount: int = Field(default=0, ge=0, lt=100)


class DishCreate(DishBase):

    """Dish create schema, iherits `DishBase`"""

    id: str | None


class DishUpdate(DishBase):
    """
    Dish update schema, inherits `DishBase`\n
    Attributes:
        title: str | None = None
        description: str | None = None
        price: Decimal | None = None
        discount: int | 0 = 0
    """

    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    discount: int = 0


class Dish(DishBase):
    """
    Dish schema, iherits `DishBase`\n
    Attributes:
        id: str
        title: str | None
        description: str | None
        price: Decimal | None
        discount: int | 0
    """

    id: str

    class Config:
        from_attributes = True
