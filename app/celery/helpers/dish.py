# import requests

# from app.config.base import DISH_LINK, DISHES_LINK, SUBMENUS_LINK


# class DishUpdate:
#     def __init__(self, submenu_data: list[dict], dish_data: list[dict]):
#         self.submenu_data = submenu_data
#         self.dish_data = dish_data
#         self.submenu_id = self.dish_data['submenu_id']
#         self.menu_id = [i['menu_id'] for i in self.submenu_data]

#     @property
#     def _menu_id(self):
#         for i in self.submenu_data:
#             if i['id'] == self.submenu_id:
#                 ...
