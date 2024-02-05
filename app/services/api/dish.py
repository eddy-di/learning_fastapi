from app.models.dish import Dish as DishModel
from app.services.cache.dish import DishCacheService
from app.services.database.dish import DishCRUD
from app.services.main import AppService


class DishService(AppService):

    def get_dishes(self, submenu_id: str) -> list[DishModel]:
        """GET operation for retrieving list of dishes related to a specific submenu"""

        if all_dishes := DishCacheService(self.cache).get_dishes():
            return all_dishes

        result = DishCRUD(self.db).get_dishes(
            submenu_id=submenu_id
        )

        DishCacheService(self.cache).set_dishes(query_result=result)

        return result
