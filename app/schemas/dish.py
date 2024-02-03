from decimal import Decimal

from pydantic import BaseModel


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
