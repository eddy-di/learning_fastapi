from fastapi.testclient import TestClient
from database import TestingRUDSessionLocal

from models import Menu, SubMenu, Dish, generate_uuid
from main import app

client = TestClient(app)


def create_submenu(menu_id, submenu_id):
    session = TestingRUDSessionLocal()
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    db_submenu_item = SubMenu(
        id=submenu_id,
        title='testSubMenu1',
        description='testSubMenu1Description',
        menu_id=db_menu_item.id
    )
    session.add(db_submenu_item)
    session.commit()
    session.close()


def create_dish(menu_id, submenu_id, dish_id):
    session = TestingRUDSessionLocal()
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    db_submenu_item = SubMenu(
        id=submenu_id,
        title='testSubMenu1',
        description='testSubMenu1Description',
        menu_id=db_menu_item.id
    )
    session.add(db_submenu_item)
    session.commit()
    db_dish_item = Dish(
        id=dish_id,
        title='testDishTitle1',
        description='testDishDescription1',
        price='11.10',
        submenu_id=db_submenu_item.id
    )
    session.add(db_dish_item)
    session.commit()
    session.close()


def test_dish_get_list(test_db):
    # given: available menu and submenu
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    create_submenu(menu_id, submenu_id)
    url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() == []


def test_dish_post(test_db):
    # given: available menu and submenu
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    create_submenu(menu_id, submenu_id)
    url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
    # when: executing CRUD operation post
    post_data = {
        "title": "testDishTitle1",
        "description": "testDishDescription1",
        "price": "12.12"
    }
    response = client.post(url, json=post_data)
    # then: expecting to get 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '12.12'


def test_dish_get_target_id(test_db):
    # given: available menu, submenu and dish
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    dish_id = generate_uuid()
    create_dish(menu_id, submenu_id, dish_id)
    url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting to get 200 and available instance data in response
    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '11.10'


def test_dish_update_target_id(test_db):
    # given: available menu, submenu and dish
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    dish_id = generate_uuid()
    create_dish(menu_id, submenu_id, dish_id)
    url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    # when: executing CRUD operation patch
    patch_data = {
        'price': '33.99'
    }
    response = client.patch(url, json=patch_data)
    # then: expecting to get 200 and changed field in response
    assert response.status_code == 200
    assert response.json()['price'] == '33.99'
    assert response.json()['title'] != '33.99'
    assert response.json()['description'] != '33.99'


def test_dish_delete_target_id(test_db):
    # given: available menu, submenu and dish
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    dish_id = generate_uuid()
    create_dish(menu_id, submenu_id, dish_id)
    url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting to get 204 status code
    assert response.status_code == 204
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting to get 404 status code and not found message
    assert response.status_code == 404
    assert response.json() == {"detail":"dish not found"}

