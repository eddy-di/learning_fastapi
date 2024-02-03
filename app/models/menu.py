from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.utils.generators import generate_uuid


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)

    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete-orphan')
