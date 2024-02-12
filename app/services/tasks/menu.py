import requests

from app.config.base import ALL_MENUS, MENU_LINK, MENUS_LINK
from app.services.tasks.parse import ExcelSheetParse

parsed_menus = ExcelSheetParse().menus


class UpdateMenu:
    def __init__(self, data: list[dict] = parsed_menus):
        self.data = data

    def get_menus_preview_db(self):
        url = ALL_MENUS
        reponse = requests.get(url).json()
        return reponse

    def get_menus_db(self):
        url = MENUS_LINK
        response = requests.get(url).json()
        return response

    def delete_menu(self, menu_instance: dict):
        url = MENU_LINK.format(target_menu_id=menu_instance['id'])
        requests.delete(url)

    def post_menus(self):
        url = MENUS_LINK
        for menu in self.data:
            new_menu_data = {
                'id': menu['id'],
                'title': menu['title'],
                'description': menu['description']
            }
            requests.post(url, json=new_menu_data)

    def get_menu(self, menu_instance: dict):
        url = MENU_LINK.format(target_menu_id=menu_instance['id'])
        response = requests.get(url)
        return response

    def patch_menu(self, menu_instance: dict):
        url = MENU_LINK.format(target_menu_id=menu_instance['id'])
        data = {
            'title': menu_instance['title'],
            'description': menu_instance['description']
        }
        requests.patch(url, json=data)

    def check_all_menus(self, parsed_data: list[dict]):
        excel_data = parsed_data
        db_data = self.get_menus_db()
        # if there are no menu objects in db
        if db_data == []:
            self.post_menus()
        # if menu got deleted from excel
        if len(excel_data) != len(db_data):
            diff = set(db_data) - set(excel_data)
            for i in iter(diff):
                self.delete_menu(menu_instance=i)
        # if something changed in menus
        for i in range(len(excel_data)):
            if excel_data[i]['id'] != db_data[i]['id'] or \
                    excel_data[i]['title'] != db_data[i]['title'] or \
                    excel_data[i]['description'] != db_data[i]['description']:
                self.patch_menu(menu_instance=excel_data[i])
