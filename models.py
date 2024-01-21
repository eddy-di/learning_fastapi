from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import engine

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, default=str(uuid4()))
    title = Column(String, index=True)
    description = Column(String, index=True)

    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, default=str(uuid4()))
    title = Column(String, index=True)
    description = Column(String, index=True)

    menu_id = Column(String, ForeignKey("menus.id", ondelete='CASCADE'))
    
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")



class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, default=str(uuid4()))
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)

    submenu_id = Column(String, ForeignKey("submenus.id", ondelete='CASCADE'))
    
    submenu = relationship('SubMenu', back_populates='dishes')


Base.metadata.create_all(bind=engine)