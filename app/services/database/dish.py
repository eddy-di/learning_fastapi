from fastapi import HTTPException
from sqlalchemy import select

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.dish import DishCreate, DishUpdate
from app.services.database.menu import not_found_exception as no_menu
from app.services.database.submenu import not_found_exception as no_submenu
from app.services.main import DatabaseCRUD


def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent dish instance."""

    raise HTTPException(status_code=404, detail='dish not found')


class DishCRUD(DatabaseCRUD):
    """Service for querying specific dish."""

    async def check_menu_id(self, menu_id: str) -> HTTPException | None:
        """Check if menu id given in endpoint is correct and exists."""

        res = await self.db.execute(
            select(
                MenuModel
            )
            .where(MenuModel.id == menu_id)
        )

        res = res.scalar()

        if not res:
            return no_menu()
        return None

    async def check_submenu_id(self, submenu_id: str) -> HTTPException | None:
        """Check if submenu id given in endpoint is correct and exists."""

        res = await self.db.execute(
            select(
                SubMenuModel
            )
            .where(SubMenuModel.id == submenu_id)
        )

        res = res.scalar()

        if not res:
            return no_submenu()
        return None

    async def fetch_dish(self, dish_id: str) -> DishModel | None:
        """Fetching specific dish by its id for furter operations."""

        query = await self.db.execute(
            select(
                DishModel
            )
            .where(DishModel.id == dish_id)
        )

        query = query.scalar()

        return query

    async def get_dishes(self, submenu_id: str) -> list[DishModel]:
        """Query to get list of all dishes."""

        result = await self.db.execute(
            select(
                DishModel
            )
            .filter(DishModel.submenu_id == submenu_id)
        )

        return result.scalars().fetchall()

    async def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_schema: DishCreate
    ) -> DishModel:
        """Create dish instance in database."""

        await self.check_menu_id(menu_id=menu_id)
        await self.check_submenu_id(submenu_id=submenu_id)

        if dish_schema.id:
            new_dish = DishModel(
                id=dish_schema.id,
                title=dish_schema.title,
                description=dish_schema.description,
                price=dish_schema.price,
                submenu_id=submenu_id
            )
        else:
            new_dish = DishModel(
                title=dish_schema.title,
                description=dish_schema.description,
                price=dish_schema.price,
                submenu_id=submenu_id
            )

        self.db.add(new_dish)

        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def get_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str
    ) -> DishModel | HTTPException:
        """Get specific dish from database."""

        await self.check_menu_id(menu_id=menu_id)
        await self.check_submenu_id(submenu_id=submenu_id)

        dish = await self.fetch_dish(dish_id=dish_id)

        if not dish:
            return not_found_exception()
        return dish

    async def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_schema: DishUpdate
    ) -> DishModel | HTTPException:
        """Update specific dish in database."""

        await self.check_menu_id(menu_id=menu_id)
        await self.check_submenu_id(submenu_id=submenu_id)

        dish_to_update = await self.fetch_dish(dish_id=dish_id)

        if not dish_to_update:
            return not_found_exception()

        for key, value in dish_schema.model_dump(exclude_unset=True).items():
            setattr(dish_to_update, key, value)

        await self.db.commit()
        await self.db.refresh(dish_to_update)
        return dish_to_update

    async def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str
    ) -> None | HTTPException:
        """Delete specific dish in database."""

        await self.check_menu_id(menu_id=menu_id)
        await self.check_submenu_id(submenu_id=submenu_id)

        dish_to_delete = await self.fetch_dish(dish_id=dish_id)

        if not dish_to_delete:
            return not_found_exception()

        await self.db.delete(dish_to_delete)
        await self.db.commit()
        return None
