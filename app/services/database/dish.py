from fastapi import HTTPException

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.dish import DishCreate, DishUpdate

from ..main import AppCRUD, AppService
from .menu import not_found_exception as no_menu
from .submenu import not_found_exception as no_submenu


def not_found_exception() -> HTTPException:
    raise HTTPException(status_code=404, detail='dish not found')


class DishService(AppService):
    def check_menu_id(self, menu_id: str) -> HTTPException:
        res = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not res:
            return no_menu()

    def check_submenu_id(self, submenu_id: str) -> HTTPException:
        res = self.db.query(SubMenuModel).filter(SubMenuModel.id == submenu_id).first()
        if not res:
            return no_submenu()

    def read_dishes(self, submenu_id: str):

        result = self.db.query(DishModel).filter(DishModel.submenu_id == submenu_id).all()

        return result


class DishCRUD(AppCRUD):
    def check_menu_id(self, menu_id: str) -> HTTPException:
        res = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not res:
            return no_menu()

    def check_submenu_id(self, submenu_id: str) -> HTTPException:
        res = self.db.query(SubMenuModel).filter(SubMenuModel.id == submenu_id).first()
        if not res:
            return no_submenu()

    def fetch_dish(self, dish_id: str):
        return self.db.query(DishModel).filter(DishModel.id == dish_id).first()

    def create_dish(self, menu_id: str, submenu_id: str, dish_schema: DishCreate):
        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        new_dish = DishModel(
            title=dish_schema.title,
            description=dish_schema.description,
            price=dish_schema.price,
            submenu_id=submenu_id
        )
        self.db.add(new_dish)
        self.db.commit()
        self.db.refresh(new_dish)
        return new_dish

    def read_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        dish = self.fetch_dish(dish_id=dish_id)

        if not dish:
            return not_found_exception()
        return dish

    def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_schema: DishUpdate):
        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        dish_to_update = self.fetch_dish(dish_id=dish_id)

        if not dish_to_update:
            return not_found_exception()

        for key, value in dish_schema.model_dump(exclude_unset=True).items():
            setattr(dish_to_update, key, value)
        self.db.commit()
        self.db.refresh(dish_to_update)
        return dish_to_update

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        dish_to_delete = self.fetch_dish(dish_id=dish_id)

        if not dish_to_delete:
            return not_found_exception()
        self.db.delete(dish_to_delete)
        self.db.commit()
        return dish_to_delete
