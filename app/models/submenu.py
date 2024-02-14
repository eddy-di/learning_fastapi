from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from app.config.database import Base
from app.utils.generators import generate_uuid


class SubMenu(Base):
    """
    SQLAlchemy model for `submenus` table in database\n
    ## Attributes:
        id -> (autogenerated) `str`\n
        title -> `str`\n
        description -> `str`\n
        menu_id -> FK to 'menus' through `menus.id`\n
        menu related to Menu model and backpopulates submenus\n
        dishes related to Dish model and backpopulates submenu
    """
    __tablename__ = 'submenus'

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    title = Column(String)
    description = Column(String)

    menu_id = Column(
        String,
        ForeignKey(
            'menus.id',
            ondelete='CASCADE'
        )
    )
    menu: Mapped['Menu'] = relationship(
        back_populates='submenus',
        lazy='selectin'
    )

    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
