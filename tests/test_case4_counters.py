from .conftest import *


menu_url = f"/api/v1/menus"

menu_id = None
submenu_id = None
dish1_id = None
dish2_id = None

def test_create_menu(init_db):
    init_db
    # given: empty db and endpoint url
    global menu_id
    url = menu_url
    # when:
    data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = client.post(url, json=data)
    # then:
    assert response.status_code == 201
    assert response.json()['title'] == 'My menu 1'
    assert response.json()['description'] == 'My menu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    menu_id = response.json()['id']
    


def test_submenu_create():
    # given:
    global menu_id
    global submenu_id
    submenus_url = menu_url + '/' + menu_id + '/submenus'
    # when:
    submenu_data = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = client.post(submenus_url, json=submenu_data)
    # then:
    assert response.status_code == 201
    assert response.json()['title'] == 'My submenu 1'
    assert response.json()['description'] == 'My submenu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    submenu_id = response.json()['id']


def test_dish_create_case1():
    # given:
    global menu_id
    global submenu_id
    global dish1_id
    dish_url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when:
    dish1_data = {
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    }
    response = client.post(dish_url, json=dish1_data)
    # then:
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 2'
    assert response.json()['description'] == 'My dish description 2'
    assert response.json()['price'] == '13.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish1_id = response.json()['id']


def test_dish_create_case2():
    # given:
    global menu_id
    global submenu_id
    global dish2_id
    dish_url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when:
    dish2_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response = client.post(dish_url, json=dish2_data)
    # then:
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 1'
    assert response.json()['description'] == 'My dish description 1'
    assert response.json()['price'] == '12.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish2_id = response.json()['id']


def test_get_counters_for_target_menu():
    # given:
    global menu_id
    url = menu_url + '/' + menu_id
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == menu_id


def test_get_counters_for_target_submenu():
    # given:
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == submenu_id


def test_delete_target_submenu():
    # given:
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id
    # when:
    response = client.delete(url)
    # then:
    assert response.status_code == 200


def test_get_submenu_list():
    # given:
    global menu_id
    url = menu_url + '/' + menu_id + '/submenus'
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json() == []


def test_get_dishes_list():
    # given:
    global menu_id
    global submenu_id
    url = menu_url + '/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json() == []


def test_get_target_menu():
    # given:
    global menu_id
    url = menu_url + '/' + menu_id 
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0
    assert response.json()['id'] == menu_id


def test_delete_target_menu():
    # given:
    global menu_id
    url = menu_url + '/' + menu_id 
    # when:
    response = client.delete(url)
    # then:
    assert response.status_code == 200


def test_get_menus_list():
    # given:
    url = menu_url 
    # when:
    response = client.get(url)
    # then:
    assert response.status_code == 200
    assert response.json() == []

def test_end(drop_db):
    drop_db
