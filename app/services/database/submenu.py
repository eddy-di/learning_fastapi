from fastapi import HTTPException
from sqlalchemy import distinct, func, select
from sqlalchemy.orm import selectinload

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate
from app.services.database.menu import not_found_exception as no_menu
from app.services.main import DatabaseCRUD


def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent submenu instance."""

    raise HTTPException(status_code=404, detail='submenu not found')


class SubMenuCRUD(DatabaseCRUD):
    """Service for querying specific submenu."""

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

    async def fetch_menus_submenu(self, submenu_id: str) -> SubMenuModel | None:
        """Fetching specific submenu by its id for furter operations."""

        query = await self.db.execute(
            select(
                SubMenuModel
            )
            .where(SubMenuModel.id == submenu_id)
        )

        query = query.scalar()

        return query

    async def get_submenus(self, menu_id: str) -> list[dict]:
        """Query to get list of all submenus."""

        await self.check_menu_id(menu_id=menu_id)

        all_submenus = await self.db.execute(
            select(
                SubMenuModel,
                func.count(distinct(DishModel.id)).label('dishes_count')
            )
            .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)
            .group_by(SubMenuModel.id)
            .where(SubMenuModel.menu_id == menu_id)
        )

        all_submenus = all_submenus.all()

        if not all_submenus:
            return []

        result = []
        for i in all_submenus:
            submenu, count = i
            result.append({
                'title': submenu.title,
                'description': submenu.description,
                'id': submenu.id,
                'dishes_count': count
            })
        return result

    async def create_submenu(
        self,
        submenu_schema: SubMenuCreate,
        menu_id: str
    ) -> SubMenuModel | HTTPException:
        """Create submenu instance in database."""

        await self.check_menu_id(menu_id)

        if submenu_schema.id:
            new_submenu = SubMenuModel(
                id=submenu_schema.id,
                title=submenu_schema.title,
                description=submenu_schema.description
            )
        else:
            new_submenu = SubMenuModel(
                title=submenu_schema.title,
                description=submenu_schema.description,
                menu_id=menu_id
            )
        self.db.add(new_submenu)

        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def get_submenu(
        self,
        menu_id: str,
        submenu_id: str
    ) -> SubMenuModel | HTTPException:
        """Get specific submenu from database."""

        await self.check_menu_id(menu_id=menu_id)

        target_submenu_query = await (
            self.db.execute(
                select(
                    SubMenuModel
                )
                .where(SubMenuModel.id == submenu_id)
                .options(
                    selectinload(SubMenuModel.dishes)
                )
            )
        )

        target_submenu = target_submenu_query.scalar()

        if not target_submenu:
            return not_found_exception()

        dishes_count_query = await (
            self.db.execute(
                select(
                    func.count(DishModel.id)
                )
                .join(SubMenuModel)
                .where(SubMenuModel.id == submenu_id)
            )
        )

        target_submenu.dishes_count = dishes_count_query.scalar()

        return target_submenu

    async def update_submenu(
        self,
        submenu_schema: SubMenuUpdate,
        menu_id: str,
        submenu_id: str
    ) -> SubMenuModel | HTTPException:
        """Update specific submenu in database."""

        await self.check_menu_id(menu_id)

        target_submenu_for_update = await self.fetch_menus_submenu(submenu_id=submenu_id)

        if not target_submenu_for_update:
            return not_found_exception()

        for key, value in submenu_schema.model_dump(exclude_unset=True).items():
            setattr(target_submenu_for_update, key, value)

        await self.db.commit()
        await self.db.refresh(target_submenu_for_update)
        return target_submenu_for_update

    async def delete_submenu(
        self,
        menu_id: str,
        submenu_id: str
    ) -> None | HTTPException:
        """Delete specific menu in database."""

        await self.check_menu_id(menu_id)

        target_submenu_for_delete = await self.fetch_menus_submenu(submenu_id=submenu_id)

        if not target_submenu_for_delete:
            return not_found_exception()

        await self.db.delete(target_submenu_for_delete)
        await self.db.commit()
        return None
