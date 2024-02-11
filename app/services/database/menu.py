from fastapi import HTTPException
from sqlalchemy import distinct, func, select
from sqlalchemy.orm import selectinload

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services.main import DatabaseCRUD


def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent menu instance."""

    raise HTTPException(status_code=404, detail='menu not found')


class MenuCRUD(DatabaseCRUD):
    """Service for querying specific menu."""

    async def get_preview(self):
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

        query = (
            select(MenuModel)
            .outerjoin(SubMenuModel, MenuModel.id == SubMenuModel.menu_id)
            .outerjoin(DishModel, SubMenuModel.id == DishModel.submenu_id)
        )
        result = await self.db.execute(query)

        all_data = result.scalars().fetchall()

        return all_data

    async def get_menus(self) -> list[dict]:
        """Query to get list of all menus."""

        menus = await (
            self.db.execute(
                select(
                    MenuModel,
                    func.count(distinct(SubMenuModel.id)).label('submenus_count'),
                    func.count(distinct(DishModel.id)).label('dishes_count'),
                )
                .join(SubMenuModel, MenuModel.id == SubMenuModel.menu_id, isouter=True)
                .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)
                .group_by(MenuModel.id, MenuModel.title, MenuModel.description)
            )
        )

        menus = menus.scalars().fetchall()

        return menus

    async def create_menu(self, menu_schema: MenuCreate) -> MenuModel:
        """Create menu instance in database."""

        new_menu = MenuModel(
            title=menu_schema.title,
            description=menu_schema.description
        )
        self.db.add(new_menu)

        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def get_menu(self, menu_id: str) -> MenuModel | HTTPException:
        """Get specific menu from database."""

        target_menu_from_db = await (
            self.db.execute(
                select(
                    MenuModel
                )
                .where(MenuModel.id == menu_id)
                .options(
                    selectinload(MenuModel.submenus)
                    .options(
                        selectinload(SubMenuModel.dishes)
                    )
                )
            )
        )

        target_menu_from_db = target_menu_from_db.scalar()

        if not target_menu_from_db:
            return not_found_exception()

        target_menu_from_db.submenus_count = await (
            self.db.execute(
                select(
                    func.count(SubMenuModel.id)
                )
                .where(SubMenuModel.menu_id == target_menu_from_db.id)
            )
        )

        target_menu_from_db = target_menu_from_db.scalar()

        target_menu_from_db.dishes_count = await (
            self.db.execute(
                select(
                    func.count(DishModel.id)
                )
                .join(SubMenuModel)
                .where(SubMenuModel.menu_id == target_menu_from_db.id)
            )
        )

        target_menu_from_db = target_menu_from_db.scalar()

        return target_menu_from_db

    async def update_menu(
        self,
        menu_id: str,
        menu_schema: MenuUpdate
    ) -> MenuModel | HTTPException:
        """Update specific menu in database."""

        target_menu_from_db = await self.db.execute(
            select(
                MenuModel
            )
            .where(MenuModel.id == menu_id)
        )

        target_menu_from_db = target_menu_from_db.scalar()

        if not target_menu_from_db:
            return not_found_exception()

        for key, value in menu_schema.model_dump(exclude_unset=True).items():
            setattr(target_menu_from_db, key, value)
        await self.db.commit()
        await self.db.refresh(target_menu_from_db)
        return target_menu_from_db

    async def delete_menu(self, menu_id: str) -> None | HTTPException:
        """Delete specific menu in database."""

        target_menu_from_db = await self.db.execute(
            select(
                MenuModel
            )
            .where(MenuModel.id == menu_id)
        )

        target_menu_from_db = target_menu_from_db.scalar()

        if not target_menu_from_db:
            return not_found_exception()

        await self.db.delete(target_menu_from_db)
        await self.db.commit()
        return None
