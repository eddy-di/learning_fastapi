import uuid

from .conftest import client

menu_url = '/api/v1/menus'

menu_id = None
submenu_id = None
dish1_id = None
dish2_id = None


def test_create_menu(init_db):
    init_db
    # given: empty db with initialized tables
    global menu_id
    url = menu_url
    # when: executing POST operation for menu instance
    data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post(url, json=data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My menu 1'
    assert response.json()['description'] == 'My menu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    menu_id = response.json()['id']


def test_submenu_create():
    # given: menu instance
    global menu_id
    global submenu_id
    submenus_url = menu_url + '/' + menu_id + '/submenus'
    # when: executing POST operation for submenu instance
    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = client.post(submenus_url, json=submenu_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My submenu 1'
    assert response.json()['description'] == 'My submenu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    submenu_id = response.json()['id']


def test_dish_create_case1():
    # given: menu and linked submenu instance
    global menu_id
    global submenu_id
    global dish1_id
    dish_url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when: executing POST operation for first dish instance
    dish1_data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    response = client.post(dish_url, json=dish1_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 2'
    assert response.json()['description'] == 'My dish description 2'
    assert response.json()['price'] == '13.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish1_id = response.json()['id']


def test_dish_create_case2():
    # given: menu and linked submenu instance
    global menu_id
    global submenu_id
    global dish2_id
    dish_url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when: executing POST operation for second dish instance
    dish2_data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = client.post(dish_url, json=dish2_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 1'
    assert response.json()['description'] == 'My dish description 1'
    assert response.json()['price'] == '12.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish2_id = response.json()['id']


def test_get_counters_for_target_menu():
    # given: menu linked with submenu and two dish instances
    global menu_id
    url = menu_url + '/' + menu_id
    # when: executing GET operation for target menu
    response = client.get(url)
    # then: expecting to get status code 200 and submenus_count == 1, dishes_count == 2
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == menu_id


def test_get_counters_for_target_submenu():
    # given: menu linked with submenu and two dish instances
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id
    # when: executing GET operation for target submenu
    response = client.get(url)
    # then: expecting to get status code 200 and dishes_count == 2
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == submenu_id


def test_delete_target_submenu():
    # given: menu linked with submenu and two dish instances
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id
    # when: executing DELETE operation for target submenu
    response = client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200


def test_get_submenu_list():
    # given: menu instance
    global menu_id
    url = menu_url + '/' + menu_id + '/submenus'
    # when: executing GET operation for submenu list
    response = client.get(url)
    # then: expecting to get status code 200 and empty submenus
    assert response.status_code == 200
    assert response.json() == []


def test_get_dishes_list():
    # given: menu instance
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when: executing GET operation for dishes list
    response = client.get(url)
    # then: expecting to get status code 200 and empty dishes
    assert response.status_code == 200
    assert response.json() == []


def test_get_target_menu():
    # given: menu instance
    global menu_id
    url = menu_url + '/' + menu_id
    # when: executing GET operation for target menu
    response = client.get(url)
    # then: expecting to get status code 200 and submenus_count == 0, dishes_count == 0
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0
    assert response.json()['id'] == menu_id


def test_delete_target_menu():
    # given: menu instance
    global menu_id
    url = menu_url + '/' + menu_id
    # when: executing DELETE operation for target menu
    response = client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200


def test_get_menus_list():
    # given: empty db
    url = menu_url
    # when: executing GET operation for menu list
    response = client.get(url)
    # then: expecting to get status code 200 and empty menus
    assert response.status_code == 200
    assert response.json() == []


def test_end(drop_db):
    # necessary to cleanup db
    drop_db
