import uuid
from fastapi.testclient import TestClient
from database import TestingRUDSessionLocal
from models import Menu, generate_uuid

from main import app

client = TestClient(app)


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

def test_menu_get_list(test_db):
    # given: empty db in test_db, client from client variable
    url = '/api/v1/menus'
    # when: executing CRUD operation get on list
    response = client.get(url)
    content = response.content.decode('utf-8')
    # then: expecting to get status code 200 and an empty list in response
    assert response.status_code == 200
    assert '[]' in content
    assert response.json() == []

def test_menu_post(test_db):
    # given: empty db in test_db, client from client variable
    url = '/api/v1/menus'
    # when: executing CRUD operation post on list with post_data
    post_data = {
        'title': 'Menu 1',
        'description': 'Menu 1 description'
    }
    response = client.post(url, json=post_data)
    # then: expecting to get status code 201 and response data being similar to post_data
    assert response.status_code == 201
    data = response.json()
        # Check if 'id' is a valid UUID4
    assert 'id' in data
    assert isinstance(uuid.UUID(data['id'], version=4), uuid.UUID)
        # Check other fields excluding 'id'
    expected_data = {
        'title': 'Menu 1',
        'description': 'Menu 1 description',
        'submenus': [],
        'submenus_count': None,
        'dishes_count': None
    }
    assert {k: data[k] for k in expected_data.keys()} == expected_data


def test_menu_get_target_menu(test_db):
    # given: an instance of menu obj
    menu_id = generate_uuid()
    create_menu(menu_id)
    # when: executing CRUD operation get on target id
    url = f'/api/v1/menus/{menu_id}'
    response = client.get(url)
    # then: expecting to get status code 200 and response data similar to provided in fixture
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['title'] == 'testMenu1'
    assert response_data['description'] == 'testMenu1Description'


def test_menu_update_target_id(test_db):
    # given: an instance of menu obj
    menu_id = generate_uuid()
    create_menu(menu_id)
    # when: executing CRUD operation patch on target id
    url = f'/api/v1/menus/{menu_id}'
    patch_data = {
        "description": "patchedMenuDescription"
    }
    response = client.patch(url, json=patch_data)
    # then: expecting to to get status code 200 and response description changed
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedMenuDescription'
    assert response.json()['submenus'] == []
    assert response.json()['submenus_count'] == None or 0
    assert response.json()['dishes_count'] == None or 0


def test_menu_delete_target_id(test_db):
    # given: an instance of menu obj
    menu_id = generate_uuid()
    create_menu(menu_id)
    url = f'/api/v1/menus/{menu_id}'
    # when: executing CRUD operation delete on target id
    response = client.delete(url)
    # then: expecting to to get status code 204 
    assert response.status_code == 204
    # when: executing CRUD operation get on  deleted target id
    response = client.get(url)
    # then: expecting to get status code 404 and not found detail
    assert response.status_code == 404
    assert response.json() == {"detail":"menu not found"}
