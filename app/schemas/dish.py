from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data):
        if 0 < data.discount <= 100:
            discounted_price = Decimal(
                data.price * (1 - Decimal(round(data.discount / 100, 2)))
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            data.price = discounted_price
        return data

    class Config:
        from_attributes = True
