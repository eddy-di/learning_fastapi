from redis import Redis
from sqlalchemy.orm import Session


class DBSessionContext:
    """
    Session of connection to database.
    """

    def __init__(self, db: Session):
        self.db = db


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    pass


class CacheSessionContext:
    def __init__(self, cache: Redis):
        self.cache = cache


class CacheService(CacheSessionContext):
    pass


class CacheCRUD(CacheSessionContext):
    pass
