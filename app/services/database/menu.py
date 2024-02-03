from sqlalchemy import distinct, func

from app.models.dish import Dish as DishModel
from app.models.menu import Menu as MenuModel
from app.models.submenu import SubMenu as SubMenuModel
from app.schemas.menu import Menu as MenuSchema
from app.schemas.menu import MenuCreate, MenuUpdate

from .main import AppCRUD, AppService


class MenuService(AppService):
    def read_menus(self) -> list[MenuSchema]:
        """
        READ / GET list of all menus
        """
        menus = self.db.query(
            MenuModel,
            func.count(distinct(SubMenuModel.id)).label('submenus_count'),
            func.count(distinct(DishModel.id)).label('dishes_count'),
        )\
            .join(SubMenuModel, MenuModel.id == SubMenuModel.menu_id, isouter=True)\
            .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)\
            .group_by(MenuModel.id, MenuModel.title, MenuModel.description)\
            .all()

        result = []
        for i in menus:
            menu, submenus_count, dishes_count = i
            res = MenuSchema(
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            result.append(res)

        return result


class MenuCRUD(AppCRUD):
    """
    Menu queries to execute Create, Retrieve, Update and Destroy commands.
    """

    def _get_target_menu(self, target_id: str):
        result = self.db.query(
            MenuModel,
            func.count(distinct(SubMenuModel.id)).label('submenus_count'),
            func.count(distinct(DishModel.id)).label('dishes_count'),
        )\
            .join(SubMenuModel, MenuModel.id == SubMenuModel.menu_id, isouter=True)\
            .join(DishModel, SubMenuModel.id == DishModel.submenu_id, isouter=True)\
            .group_by(MenuModel.id, MenuModel.title, MenuModel.description)\
            .filter(MenuModel.id == target_id).first()
        return result

    def create_menu(self, menu_endpoint: MenuCreate) -> MenuModel:
        """
        CREATE / POST
        """
        new_menu = MenuModel(
            title=menu_endpoint.title,
            description=menu_endpoint.description
        )
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def get_menu(self, target_menu_id: str) -> MenuModel | None:
        """
        READ / GET menu by id
        """
        target_menu_from_db = self._get_target_menu(target_id=target_menu_id)

        if target_menu_from_db:
            return target_menu_from_db
        return None

    def update_menu(self, target_menu_id: str, menu_schema: MenuUpdate) -> MenuModel | None:
        """
        UPDATE / PATCH menu by id
        """
        target_menu_from_db = self.db.query(MenuModel).filter(MenuModel.id == target_menu_id).first()

        if target_menu_from_db:
            for key, value in menu_schema.model_dump(exclude_unset=True).items():
                setattr(target_menu_from_db, key, value)
            self.db.commit()
            self.db.refresh(target_menu_from_db)
        return None

    def delete_menu(self, target_menu_id: str):
        """
        DELETE menu by id
        """
        target_menu_from_db = self.db.query(MenuModel).filter(MenuModel.id == target_menu_id).first()

        if target_menu_from_db:
            self.db.delete(target_menu_from_db)
            self.db.commit()
        return None
