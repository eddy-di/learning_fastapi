from sqlalchemy import DECIMAL, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.utils.generators import generate_uuid


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)
    price = Column(DECIMAL(precision=10, scale=2))

    submenu_id = Column(String, ForeignKey('submenus.id', ondelete='CASCADE'))
    submenu = relationship('SubMenu', back_populates='dishes')