from fastapi import Depends, FastAPI

from app.config.database import Base, engine, get_db
from app.routers import dish, menu, submenu

description = """
# Menu management applications API\n
\n
This API is created solely to fulfill the requirements for completing an intensive course at Y-Lab to get internship.\n
It consists of main Menu, that can have Submenus, which in its own accord has dishes with prices.\n
\n
## Menus\n
\n
You can `GET` list of menus, `POST` a menu, `GET`, `PATCH` or `DELETE` specific menu.\n
\n
## Submenus\n
\n
You can `GET` list of submenus in a menu, `POST` a submenu in a menu, `GET`, `PATCH` or `DELETE` specific submenu in a menu.\n
\n
## Dishes\n
\n
You can `GET` list of dishes in submenu, `POST` a dish in submenu, `GET`, `PATCH` or `DELETE` specific dish in submenu.\n
"""

app = FastAPI(
    title='Y-lab intensive course API',
    description=description,
    version='3.1.8',
    dependencies=[Depends(get_db)],
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
    ]
)

Base.metadata.create_all(bind=engine)


app.include_router(menu.menu_router)
app.include_router(submenu.submenu_router)
app.include_router(dish.dish_router)
