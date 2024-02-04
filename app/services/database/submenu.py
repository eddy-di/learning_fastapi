from fastapi import HTTPException
from sqlalchemy import distinct, func

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate

from ..main import AppCRUD, AppService
from .menu import not_found_exception as no_menu


def not_found_exception() -> HTTPException:
    raise HTTPException(status_code=404, detail='submenu not found')


class SubMenuService(AppService):
    def check_menu_id(self, menu_id: str) -> HTTPException:
        res = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not res:
            return no_menu()

    def read_submenus(self, menu_id: str) -> list[dict]:
        self.check_menu_id(menu_id)

        all_submenus = self.db.query(
            SubMenuModel,
            func.count(distinct(DishModel.id)).label('dishes_count'),
        )\
            .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)\
            .group_by(SubMenuModel.id)\
            .all()

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


class SubMenuCRUD(AppCRUD):
    def check_menu_id(self, menu_id: str) -> HTTPException:
        res = self.db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not res:
            return no_menu()

    def fetch_menus_submenu(self, submenu_id: str):
        return self.db.query(SubMenuModel).filter(SubMenuModel.id == submenu_id).first()

    def create_submenu(self, submenu_schema: SubMenuCreate, menu_id: str):
        self.check_menu_id(menu_id)

        new_submenu = SubMenuModel(
            title=submenu_schema.title,
            description=submenu_schema.description,
            menu_id=menu_id
        )
        self.db.add(new_submenu)
        self.db.commit()
        self.db.refresh(new_submenu)
        return new_submenu

    def read_submenu(self, menu_id: str, submenu_id: str):
        self.check_menu_id(menu_id=menu_id)

        submenu_with_counter = self.db.query(SubMenuModel).filter(SubMenuModel.id == submenu_id).first()
        if not submenu_with_counter:
            return not_found_exception()
        submenu_with_counter.dishes_count = self.db.query(
            func.count(DishModel.id)
        ).join(SubMenuModel)\
            .filter(SubMenuModel.id == submenu_with_counter.id).scalar()

        return submenu_with_counter

    def update_submenu(self, submenu_schema: SubMenuUpdate, menu_id: str, submenu_id: str):
        self.check_menu_id(menu_id)

        target_submenu_for_update = self.fetch_menus_submenu(submenu_id=submenu_id)

        if not target_submenu_for_update:
            return not_found_exception()

        for key, value in submenu_schema.model_dump(exclude_unset=True).items():
            setattr(target_submenu_for_update, key, value)
        self.db.commit()
        self.db.refresh(target_submenu_for_update)
        return target_submenu_for_update

    def delete_submenu(self, menu_id: str, submenu_id: str):
        self.check_menu_id(menu_id)

        target_submenu_for_delete = self.fetch_menus_submenu(submenu_id=submenu_id)

        if not target_submenu_for_delete:
            return not_found_exception()
        self.db.delete(target_submenu_for_delete)
        self.db.commit()
        return target_submenu_for_delete
