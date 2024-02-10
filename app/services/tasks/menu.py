from app.config.database import AsyncSessionLocal
from app.models.menu import Menu


def save_menu_to_db(menu_instance: Menu):
    with AsyncSessionLocal() as db:
        instance = menu_instance
        db.add(instance)
        db.commit()
