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
