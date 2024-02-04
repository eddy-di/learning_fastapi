import uuid

from app.routers.menu import (
    create_menu,
    delete_menu,
    read_menu,
    read_menus,
    update_menu,
)
from app.utils.pathfinder import reverse


# testing CRUD for Menu endpoints
def test_menu_get_list(setup_test_db):
    client = setup_test_db
    # given: empty db in , client from client variable
    url = reverse(read_menus)
    # when: executing CRUD operation get on list
    response = client.get(url)
    content = response.content.decode('utf-8')
    # then: expecting to get status code 200 and an empty list in response
    assert response.status_code == 200
    assert '[]' in content
    assert response.json() == []


def test_menu_get_list_with_submenu_and_dishes(setup_test_db, create_menu, create_dish, create_submenu):
    # given: an instance of menu, submenu and dish objs
    menu = create_menu
    submenu1 = create_submenu(menu.id)
    submenu2 = create_submenu(menu.id)
    create_dish(submenu1.id)
    create_dish(submenu2.id)
    create_dish(submenu2.id)
    client = setup_test_db
    # when: executing CRUD operation get on menus list
    url = reverse(read_menus)
    response = client.get(url)
    # then: expecting to get status code 200 and data on available instances of each objects
    assert response.status_code == 200
    assert response.json()[0]['id'] == menu.id
    assert response.json()[0]['title'] == 'testMenu1'
    assert response.json()[0]['description'] == 'testMenu1Description'
    assert response.json()[0]['submenus_count'] == 2
    assert response.json()[0]['dishes_count'] == 3


def test_menu_get_list_with_no_submenu_and_dishes(setup_test_db, create_menu):
    # given: an instance of menu obj with empty submenu and dishes
    create_menu
    client = setup_test_db
    url = reverse(read_menus)
    # when: executing CRUD operation get on menus list
    response = client.get(url)
    # then: expecting to get status code 200 and not empty list
    assert response.status_code == 200
    assert response.json() != []


def test_menu_post(setup_test_db):
    # given: empty db in , client from client variable
    client = setup_test_db
    url = reverse(create_menu)
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
        'submenus_count': 0,
        'dishes_count': 0
    }
    assert {k: data[k] for k in expected_data.keys()} == expected_data


def test_menu_get_target_id(setup_test_db, create_menu):
    # given: an instance of menu obj
    menu = create_menu
    client = setup_test_db
    # when: executing CRUD operation get on target id
    url = reverse(read_menu, target_menu_id=menu.id)
    response = client.get(url)
    # then: expecting to get status code 200 and response data similar to provided in fixture
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['title'] == 'testMenu1'
    assert response_data['description'] == 'testMenu1Description'


def test_menu_patch_target_id(setup_test_db, create_menu):
    # given: an instance of menu obj
    menu = create_menu
    client = setup_test_db
    # when: executing CRUD operation patch on target id
    url = reverse(update_menu, target_menu_id=menu.id)
    patch_data = {
        'description': 'patchedMenuDescription'
    }
    response = client.patch(url, json=patch_data)
    # then: expecting to to get status code 200 and response description changed
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedMenuDescription'
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_menu_delete_target_id(setup_test_db, create_menu):
    # given: an instance of menu obj
    menu = create_menu
    client = setup_test_db
    url = reverse(delete_menu, target_menu_id=menu.id)
    # when: executing CRUD operation delete on target id
    response = client.delete(url)
    # then: expecting to to get status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get on  deleted target id
    response = client.get(url)
    # then: expecting to get status code 404 and not found detail
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
