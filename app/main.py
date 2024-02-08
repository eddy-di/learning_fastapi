from fastapi import Depends, FastAPI

from app.config.database import Base, engine, get_db
from app.routers import dish, menu, preview, submenu

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
    dependencies=[Depends(get_db)],
    openapi_tags=[
        {
            'name': 'Preview',
            'description': 'GET opreation for getting all objects'
        },
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
    ]
)

Base.metadata.create_all(bind=engine)


app.include_router(preview.main_router)
app.include_router(menu.menu_router)
app.include_router(submenu.submenu_router)
app.include_router(dish.dish_router)
