from redis.asyncio import Redis
from sqlalchemy.orm import Session


class ServiceSessionContext:
    """Context for database session and redis."""

    def __init__(self, db: Session, cache: Redis) -> None:
        """Initialization for session of connection to database and redis."""

        self.db = db
        self.cache = cache


class AppService(ServiceSessionContext):
    pass


class DBSessionContext:
    """Context for database session."""

    def __init__(self, db: Session) -> None:
        """Initialization for session of connection to database."""

        self.db = db


class DatabaseCRUD(DBSessionContext):
    pass


class CacheSessionContext:
    """Context for cache database session."""

    def __init__(self, cache: Redis) -> None:
        """Initialization for session of connection to cache database."""

        self.cache = cache


class CacheCRUD(CacheSessionContext):
    pass
