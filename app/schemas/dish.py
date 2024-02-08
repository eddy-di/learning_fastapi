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

    pass


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

    @property
    def modified_price(self):
        if 0 < self.discount <= 100:
            return self.price * (1 - Decimal(self.discount) / 100)
        return self.price


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

    @property
    def modified_price(self):
        if 0 < self.discount <= 100:
            return self.price * (1 - Decimal(self.discount) / 100)
        return self.price

    class Config:
        from_attributes = True
