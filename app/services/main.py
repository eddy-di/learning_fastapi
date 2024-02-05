from redis import Redis
from sqlalchemy.orm import Session


class DBSessionContext:
    """Context for database session."""

    def __init__(self, db: Session) -> None:
        """Initialization for session of connection to database."""

        self.db = db


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    pass


class CacheSessionContext:
    """Context for cache database session."""

    def __init__(self, cache: Redis) -> None:
        """Initialization for session of connection to cache database."""

        self.cache = cache


class CacheService(CacheSessionContext):
    pass


class CacheCRUD(CacheSessionContext):
    pass
