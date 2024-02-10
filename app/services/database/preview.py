from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.services.main import DatabaseCRUD


class PreviewDatabase(DatabaseCRUD):
    """Service for querying all available objects in database."""

    async def get_all(self):
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

        all = await self.db.execute(
            select(
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
        )

        return all.all()
