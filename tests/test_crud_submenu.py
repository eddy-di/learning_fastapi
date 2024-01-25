from fastapi.testclient import TestClient
import uuid
from database import TestingRUDSessionLocal
from models import Menu, SubMenu

from main import app

client = TestClient(app)


def generate_uuid():
    return str(uuid.uuid4())


def create_menu(id: str):
    session = TestingRUDSessionLocal()
    db_menu_item = Menu(
        id=id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.close()


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


def test_submenu_get_list(test_db):
    # given: menu instance
    id = str(uuid.uuid4)
    create_menu(id)
    url = f'/api/v1/menus/{id}/submenus'
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting status code 200 and empty list in response
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_post(test_db):
    # given: menu instance
    id = str(uuid.uuid4)
    create_menu(id)
    url = f'/api/v1/menus/{id}/submenus'
    # when: executing CRUD operation post
    post_data = {
        "title": "subMenuTitle1",
        "description": "subMenuDescription1"
    }
    response = client.post(url, json=post_data)
    # then: expecting status code 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'subMenuTitle1'
    assert response.json()['description'] == 'subMenuDescription1'


def test_submenu_get_target_id(test_db):
    # given: menu and submenu instances
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    create_submenu(menu_id, submenu_id)
    url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting status code 200 and create_menu info in response
    assert response.status_code == 200
    assert response.json()['title'] == "testSubMenu1"
    assert response.json()['description'] == "testSubMenu1Description"
    assert response.json()['id'] == submenu_id


def test_submenu_update_target_id(test_db):
    # given: menu and submenu instances
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    create_submenu(menu_id, submenu_id)
    url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
    # when: executing CRUD operation patch
    patch_data = {
        'description': 'patchedSubMenuDescriptionData1'
    }
    response = client.patch(url, json=patch_data)
    # then: expecting status code 200 and patched info in response
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedSubMenuDescriptionData1'
    assert response.json()['title'] != 'patchedSubMenuData1'


def test_submenu_delete_taget_id(test_db):
    # given: menu and submenu instances
    menu_id = generate_uuid()
    submenu_id = generate_uuid()
    create_submenu(menu_id, submenu_id)
    url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting status code 204 
    assert response.status_code == 204 # deletion status code
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting status code 404 and not found details
    assert response.status_code == 404
    assert response.json() == {"detail":"submenu not found"}
