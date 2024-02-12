from fastapi import Depends, FastAPI

from app.celery.tasks import update_db_menu
from app.config.database import get_async_db, init_db
from app.routers import dish, menu, submenu

description = """
# Menu management applications API
This API is created solely to fulfill the requirements for completing an intensive course at Y-Lab to get internship.
It consists of Preview part that gives list of evertyhing in database, main Menu that can have Submenus, which in its own accord has Dishes with prices.\n
## Preview
Gives an access to all available objects in database through `GET` method.
## Menus
You can `GET` list of menus, `POST` a menu, `GET`, `PATCH` or `DELETE` specific menu.
## Submenus
You can `GET` list of submenus in a menu, `POST` a submenu in a menu, `GET`, `PATCH` or `DELETE` specific submenu in a menu.
## Dishes
You can `GET` list of dishes in submenu, `POST` a dish in submenu, `GET`, `PATCH` or `DELETE` specific dish in submenu.
"""


app = FastAPI(
    title='Y-lab intensive course API',
    description=description,
    version='3.1.8',
    dependencies=[Depends(get_async_db), ],
    openapi_tags=[
        {
            'name': 'Menus',
            'description': 'Operations for menus'
        },
        {
            'name': 'Submenus',
            'description': 'Operations for submenus'
        },
        {
            'name': 'Dishes',
            'description': 'Operations for dishes'
        }
    ],
)


@app.on_event('startup')
async def on_startup():
    await init_db()

    update_db_menu.delay()


app.include_router(menu.menu_router)
app.include_router(submenu.submenu_router)
app.include_router(dish.dish_router)
