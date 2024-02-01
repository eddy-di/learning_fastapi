from fastapi import FastAPI, Depends
from app.routers import menu, submenu, dish
from app.database.database import get_db, Base, engine



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
