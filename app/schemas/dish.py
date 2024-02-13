from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, Field, ValidationInfo, field_validator


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
    """
    Dish update schema, inherits `DishBase`\n
    Attributes:
        title: str | None = None
        description: str | None = None
        price: Decimal | None = None
        discount: int | 0 = 0
        ---adding to the model---
        id: str | None
    """

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
    discount: int = Field(default=0, ge=0, lt=100)


class Dish(DishBase):
    """
    Dish schema, iherits `DishBase`\n
    Attributes:
        title: str | None
        description: str | None
        price: Decimal | None
        discount: int | 0
        ---adding to the model---
        id: str | None
    """

    id: str

    @field_validator('price')
    @classmethod
    def discounted_price(cls, value: Decimal, info: ValidationInfo):
        discount = info.data['discount']
        if 0 < discount <= 100:
            discounted_price = Decimal(
                value * (1 - Decimal(round(discount / 100, 2)))
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            value = discounted_price
        return value

    class Config:
        from_attributes = True
