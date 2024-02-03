from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.utils.generators import generate_uuid


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)

    menu_id = Column(String, ForeignKey('menus.id', ondelete='CASCADE'))
    menu = relationship('Menu', back_populates='submenus')

    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')
