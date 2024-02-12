# import requests

# from app.config.base import SUBMENU_LINK, SUBMENUS_LINK


# class UpdateSubmenu:
#     def __init__(self, data: list[dict]):
#         self.data = data
#         self.menu_id = self.data['menu_id']
#         self.url = SUBMENUS_LINK.format(target_menu_id=self.menu_id)

#     def get_submenus_db(self):
#         url = self.url
#         response = requests.get(url)
#         return response

#     def patch_submenu(self, submenu_instance: str):
#         url = SUBMENU_LINK.format(
#             target_menu_id=self.menu_id,
#             target_submenu_id=submenu_instance['id']
#         )
#         data = {
#             'title': submenu_instance['title'],
#             'description': submenu_instance['description']
#         }
#         requests.patch(url, json=data)

#     def delete_submenu(self, submenu_instance: str):
#         url = SUBMENU_LINK.format(
#             target_menu_id=self.menu_id,
#             target_submenu_id=submenu_instance['id']
#         )
#         requests.delete(url)

#     def post_submenus(self):
#         url = self.url
#         for submenu in self.data:
#             new_submenu_data = {
#                 'id': submenu['id'],
#                 'title': submenu['title'],
#                 'description': submenu['description']
#             }
#             requests.post(url, json=new_submenu_data)

#     def check_all_submenus(self):
#         excel_data = self.data
#         db_data = self.get_submenus_db()
#         # if there are no menu objects in db
#         if db_data == []:
#             self.post_submenus()
#         # if menu got deleted from excel
#         if len(excel_data) != len(db_data):
#             diff = set(db_data) - set(excel_data)
#             for i in iter(diff):
#                 self.delete_submenu(submenu_instance=i)
#         # if something changed in menus
#         for i in range(len(excel_data)):
#             if excel_data[i]['id'] != db_data[i]['id'] or \
#                     excel_data[i]['title'] != db_data[i]['title'] or \
#                     excel_data[i]['description'] != db_data[i]['description']:
#                 self.patch_submenu(submenu_instance=excel_data[i])
