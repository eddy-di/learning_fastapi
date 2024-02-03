from fastapi import Depends, FastAPI

from app.database.database import Base, engine, get_db
from app.routers import dish, menu, submenu

app = FastAPI(
    title='Y-lab intensive course API',
    description='Приложение для управления меню',
    version='2.3.6',
    dependencies=[Depends(get_db)]
)

Base.metadata.create_all(bind=engine)


app.include_router(menu.menu_router)
app.include_router(submenu.submenu_router)
app.include_router(dish.dish_router)
