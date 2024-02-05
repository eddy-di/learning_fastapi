from fastapi import HTTPException
from sqlalchemy import distinct, func
from sqlalchemy.orm import selectinload

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services.main import AppCRUD, AppService


def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent menu instance."""

    raise HTTPException(status_code=404, detail='menu not found')


class MenuService(AppService):
    """Service for querying the list of all menus."""

    def get_menus(self) -> list[dict]:
        """Query to get list of all menus."""

        menus = (
            self.db.query(
                MenuModel,
                func.count(distinct(SubMenuModel.id)).label('submenus_count'),
                func.count(distinct(DishModel.id)).label('dishes_count'),
            )
            .join(SubMenuModel, MenuModel.id == SubMenuModel.menu_id, isouter=True)
            .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)
            .group_by(MenuModel.id, MenuModel.title, MenuModel.description)
            .all()
        )

        result = []
        for i in menus:
            menu, submenus_count, dishes_count = i
            result.append({
                'title': menu.title,
                'description': menu.description,
                'id': menu.id,
                'submenus_count': submenus_count,
                'dishes_count': dishes_count
            })

        return result


class MenuCRUD(AppCRUD):
    """Service for querying specific menu."""

    def create_menu(self, menu_schema: MenuCreate) -> MenuModel:
        """Create menu instance in database."""

        new_menu = MenuModel(
            title=menu_schema.title,
            description=menu_schema.description
        )
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def get_menu(self, menu_id: str) -> MenuModel | HTTPException:
        """Get specific menu from database."""

        target_menu_from_db = (
            self.db.query(MenuModel)
            .filter(MenuModel.id == menu_id)
            .options(
                selectinload(MenuModel.submenus)
                .options(
                    selectinload(SubMenuModel.dishes)
                )
            )
            .first()
        )

        if not target_menu_from_db:
            return not_found_exception()

        target_menu_from_db.submenus_count = (
            self.db.query(
                func.count(SubMenuModel.id)
            )
            .filter(SubMenuModel.menu_id == target_menu_from_db.id)
            .scalar()
        )

        target_menu_from_db.dishes_count = (
            self.db.query(
                func.count(DishModel.id)
            )
            .join(SubMenuModel)
            .filter(SubMenuModel.menu_id == target_menu_from_db.id)
            .scalar()
        )

        return target_menu_from_db

    def update_menu(
        self,
        menu_id: str,
        menu_schema: MenuUpdate
    ) -> MenuModel | HTTPException:
        """Update specific menu in database."""

        target_menu_from_db = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()

        if not target_menu_from_db:
            return not_found_exception()
        for key, value in menu_schema.model_dump(exclude_unset=True).items():
            setattr(target_menu_from_db, key, value)
        self.db.commit()
        self.db.refresh(target_menu_from_db)
        return target_menu_from_db

    def delete_menu(self, menu_id: str) -> None | HTTPException:
        """Delete specific menu in database."""

        target_menu_from_db = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()

        if not target_menu_from_db:
            return not_found_exception()

        self.db.delete(target_menu_from_db)
        self.db.commit()
        return None
