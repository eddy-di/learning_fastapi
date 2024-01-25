import uuid
from fastapi.testclient import TestClient
from database import TestingRUDSessionLocal
from models import Menu

from main import app

client = TestClient(app)

def test_menu_get_list(test_db):
    # given: empty db in test_db, client from client variable, get and post endpoint in url
    url = '/api/v1/menus'
    # when: accessing the get endpoint
    response = client.get(url)
    content = response.content.decode('utf-8')
    # then: expecting the code 200 and an empty list in the response because db is empty
    assert response.status_code == 200
    assert '[]' in content
    assert response.json() == []

def test_menu_post(test_db):
    # given: empty db in test_db, client from client variable, get and post endpoint in url
    url = '/api/v1/menus'
    # when: creating menu1 in the post endpoint with post_data
    post_data = {
        'title': 'Menu 1',
        'description': 'Menu 1 description'
    }
    response = client.post(url, json=post_data)
    # then: expecting the post_data in the response, 201 code and other uuid info formed automatically
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
    # given: a test session with created menu obj
    session = TestingRUDSessionLocal()
    menu_id = str(uuid.uuid4())
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.close()
    # when: accessing the item by its menu_id
    url = f'/api/v1/menus/{menu_id}'
    response = client.get(url)
    # then: expecting to see the information provided to be available in response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['title'] == 'testMenu1'
    assert response_data['description'] == 'testMenu1Description'


def test_menu_update_target_id(test_db):
    # given: a test session with created menu obj
    session = TestingRUDSessionLocal()
    menu_id = str(uuid.uuid4())
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.close()
    # when: trying to change the title of a menu item
    url = f'/api/v1/menus/{menu_id}'
    patch_data = {
        "title" : "patchedTitle",
        "description": "patchedMenuDescription"
    }
    response = client.patch(url, json=patch_data)
    # then: expecting to get code 200 and the patched title
    assert response.status_code == 200
    assert response.json()['title'] == 'patchedTitle'
    assert response.json()['description'] == 'patchedMenuDescription'
    assert response.json()['submenus'] == []
    assert response.json()['submenus_count'] == None or 0
    assert response.json()['dishes_count'] == None or 0


def test_menu_delete_target_id(test_db):
    # given: a test session with created menu obj
    session = TestingRUDSessionLocal()
    menu_id = str(uuid.uuid4())
    db_menu_item = Menu(
        id=menu_id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.close()
    # when: deleting a menu item and then trying to get it
    url = f'/api/v1/menus/{menu_id}'
    response = client.delete(url)
    response = client.get(url)
    # then: expecting to return 404 error because menu item was deleted
    assert response.status_code == 404
    assert response.json() == {"detail":"menu not found"}
