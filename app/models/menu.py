from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from app.config.database import Base
from app.utils.generators import generate_uuid


class Menu(Base):
    """
    SQLAlchemy model for `menus` table in database\n
    id -> (autogenerated) `str`\n
    title -> `str`\n
    description -> `str`\n
    submenus related to SubMenu model that backpopulates with menu
    """
    __tablename__ = 'menus'

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    title = Column(String)
    description = Column(String)

    submenus: Mapped[list['SubMenu']] = relationship(
        back_populates='menu',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
