from database import Base, engine
from sqlalchemy import Column, ForeignKey, String, DECIMAL
from sqlalchemy.orm import relationship
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)

    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)

    menu_id = Column(String, ForeignKey("menus.id", ondelete='CASCADE'))
    menu = relationship('Menu', back_populates='submenus')

    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")



class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    description = Column(String)
    price = Column(DECIMAL(precision=10, scale=2))

    submenu_id = Column(String, ForeignKey("submenus.id", ondelete='CASCADE'))
    submenu = relationship('SubMenu', back_populates='dishes')

