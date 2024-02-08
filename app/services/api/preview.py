from app.models.menu import Menu
from app.services.cache.preview import PreviewCache
from app.services.database.preview import PreviewDatabase
from app.services.main import AppService


class PreviewService(AppService):

    def get_all(self) -> list[Menu]:

        if everything := PreviewCache(self.cache).get_all():
            return everything

        result = PreviewDatabase(self.db).get_all()

        PreviewCache(self.cache).set_all(query_result=result)

        return result
