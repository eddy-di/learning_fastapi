from fastapi import HTTPException

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.dish import DishCreate, DishUpdate
from app.services.database.menu import not_found_exception as no_menu
from app.services.database.submenu import not_found_exception as no_submenu
from app.services.main import AppCRUD, AppService


def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent dish instance."""

    raise HTTPException(status_code=404, detail='dish not found')


class DishService(AppService):
    """Service for querying the list of all dishes."""

    def read_dishes(self, submenu_id: str) -> list[DishModel]:
        """Query to get list of all dishes."""

        result = self.db.query(DishModel).filter(DishModel.submenu_id == submenu_id).all()

        return result


class DishCRUD(AppCRUD):
    """Service for querying specific dish."""

    def check_menu_id(self, menu_id: str) -> HTTPException | None:
        """Check if menu id given in endpoint is correct and exists."""

        res = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not res:
            return no_menu()
        return None

    def check_submenu_id(self, submenu_id: str) -> HTTPException | None:
        """Check if submenu id given in endpoint is correct and exists."""

        res = self.db.query(SubMenuModel).filter(SubMenuModel.id == submenu_id).first()
        if not res:
            return no_submenu()
        return None

    def fetch_dish(self, dish_id: str) -> DishModel | None:
        """Fetching specific dish by its id for furter operations."""

        return self.db.query(DishModel).filter(DishModel.id == dish_id).first()

    def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_schema: DishCreate
    ) -> DishModel:
        """Create dish instance in database."""

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

    def read_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str
    ) -> DishModel | HTTPException:
        """Get specific dish from database."""

        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        dish = self.fetch_dish(dish_id=dish_id)

        if not dish:
            return not_found_exception()
        return dish

    def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_schema: DishUpdate
    ) -> DishModel | HTTPException:
        """Update specific dish in database."""

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

    def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str
    ) -> None | HTTPException:
        """Delete specific dish in database."""

        self.check_menu_id(menu_id=menu_id)

        self.check_submenu_id(submenu_id=submenu_id)

        dish_to_delete = self.fetch_dish(dish_id=dish_id)

        if not dish_to_delete:
            return not_found_exception()
        self.db.delete(dish_to_delete)
        self.db.commit()
        return None
