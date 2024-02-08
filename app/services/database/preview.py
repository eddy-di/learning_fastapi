from sqlalchemy import Row
from sqlalchemy.orm import selectinload

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.services.main import DatabaseCRUD


class PreviewDatabase(DatabaseCRUD):
    """Service for querying all available objects in database."""

    def get_all(self) -> list[Row[tuple[MenuModel, SubMenuModel, DishModel]]]:
        """
        Returns result of a PostgreSQl query:
            SELECT
                menus.*,
                submenus.*,
                dishes.*
            FROM
                menus
            LEFT JOIN
                submenus ON menus.id = submenus.menu_id
            LEFT JOIN
                dishes ON submenus.id = dishes.submenu_id;
        """

        all = (
            self.db.query(
                MenuModel
            )
            .options(
                selectinload(
                    MenuModel.submenus
                )
                .options(
                    selectinload(SubMenuModel.dishes)
                )
            )
            .order_by(MenuModel.id)
            .all()
        )

        return all
