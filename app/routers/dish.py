from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.base import DISH_LINK, DISHES_LINK
from app.config.database import get_db
from app.schemas.dish import Dish as DishSchema
from app.schemas.dish import DishCreate as DishCreateSchema
from app.schemas.dish import DishUpdate as DishUpdateSchema
from app.services.database.dish import DishCRUD, DishService

dish_router = APIRouter()


@dish_router.get(
    DISHES_LINK,
    response_model=list[DishSchema],
    tags=['Dishes']
)
def read_dishes(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db)
):
    """
    GET operation for retrieving list of dishes related to a specific submenu
    """
    result = DishService(db).read_dishes(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id
    )

    return result


@dish_router.post(
    DISHES_LINK,
    response_model=DishSchema,
    status_code=201,
    tags=['Dishes']
)
def create_dish(
    target_menu_id: str,
    target_submenu_id: str,
    dish: DishCreateSchema,
    db: Session = Depends(get_db)
):
    """
    POST operation for creating a new dish under a specific submenu
    """
    result = DishCRUD(db).create_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_schema=dish
    )

    return result


@dish_router.get(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes']
)
def read_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: Session = Depends(get_db)
):
    """
    GET operation for retrieving a specific dish of a specific submenu
    """
    result = DishCRUD(db).read_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )

    return result


@dish_router.patch(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes']
)
def update_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    dish_update: DishUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    PATCH operation for updating a specific dish of a specific submenu
    """
    result = DishCRUD(db).update_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id,
        dish_schema=dish_update
    )

    return result


@dish_router.delete(
    DISH_LINK,
    response_model=DishSchema,
    tags=['Dishes']
)
def delete_dish(
    target_menu_id: str,
    target_submenu_id: str,
    target_dish_id: str,
    db: Session = Depends(get_db)
):
    """
    DELETE operation for deleting a specific dish of a specific submenu
    """
    result = DishCRUD(db).delete_dish(
        menu_id=target_menu_id,
        submenu_id=target_submenu_id,
        dish_id=target_dish_id
    )

    return result
