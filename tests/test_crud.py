from .conftest import *
import uuid


# testing CRUD for Menu endpoints
def test_menu_get_list(setup_test_db):
    client = setup_test_db
    # given: empty db in , client from client variable
    url = '/api/v1/menus'
    # when: executing CRUD operation get on list
    response = client.get(url)
    content = response.content.decode('utf-8')
    # then: expecting to get status code 200 and an empty list in response
    assert response.status_code == 200
    assert '[]' in content
    assert response.json() == []


def test_menu_get_list_with_data_in_db(setup_test_db):
    # given: an instance of menu, submenu and dish objs
    menu = create_menu()
    submenu1 = create_submenu(menu.id)
    submenu2 = create_submenu(menu.id)
    create_dish(submenu1.id)
    create_dish(submenu2.id)
    create_dish(submenu2.id)
    client = setup_test_db
    # when: executing CRUD operation get on menus list
    url = '/api/v1/menus'
    response = client.get(url)
    # then: expecting to get status code 200 and data on available instances of each objects
    assert response.status_code == 200
    assert response.json()[0]['id'] == menu.id
    assert response.json()[0]['title'] == 'testMenu1'
    assert response.json()[0]['description'] == 'testMenu1Description'
    assert response.json()[0]['submenus_count'] == 2
    assert response.json()[0]['dishes_count'] == 3


def test_menu_post(setup_test_db):
    # given: empty db in , client from client variable
    client = setup_test_db
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
        'submenus_count': 0,
        'dishes_count': 0
    }
    assert {k: data[k] for k in expected_data.keys()} == expected_data




def test_menu_get_target_id(setup_test_db):
    # given: an instance of menu obj
    menu = create_menu()
    client = setup_test_db
    # when: executing CRUD operation get on target id
    url = f'/api/v1/menus/{menu.id}'
    response = client.get(url)
    # then: expecting to get status code 200 and response data similar to provided in fixture
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['title'] == 'testMenu1'
    assert response_data['description'] == 'testMenu1Description'


def test_menu_patch_target_id(setup_test_db):
    # given: an instance of menu obj
    menu = create_menu()
    client = setup_test_db
    # when: executing CRUD operation patch on target id
    url = f'/api/v1/menus/{menu.id}'
    patch_data = {
        "description": "patchedMenuDescription"
    }
    response = client.patch(url, json=patch_data)
    # then: expecting to to get status code 200 and response description changed
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedMenuDescription'
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_menu_delete_target_id(setup_test_db):
    # given: an instance of menu obj
    menu = create_menu()
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}'
    # when: executing CRUD operation delete on target id
    response = client.delete(url)
    # then: expecting to to get status code 200 
    assert response.status_code == 200
    # when: executing CRUD operation get on  deleted target id
    response = client.get(url)
    # then: expecting to get status code 404 and not found detail
    assert response.status_code == 404
    assert response.json() == {"detail":"menu not found"}


# testing CRUD for submenus endpoints
def test_submenu_get_list(setup_test_db):
    # given: menu instance
    menu = create_menu()
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}/submenus'
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting status code 200 and empty list in response
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_get_list_with_data_in_db(setup_test_db):
    # given: an instance of menu, submenu and dish objs
    client = setup_test_db
    menu = create_menu()
    submenu = create_submenu(menu.id)
    create_dish(submenu.id)
    # when: executing CRUD operation get on menus list
    url = f'/api/v1/menus/{menu.id}/submenus'
    response = client.get(url)
    # then: expecting to get status code 200 and data on available instances of each objects
    assert response.status_code == 200
    assert response.json()[0]['id'] == submenu.id
    assert response.json()[0]['title'] == 'testSubMenu1'
    assert response.json()[0]['description'] == 'testSubMenu1Description'
    assert response.json()[0]['dishes_count'] == 1


def test_submenu_post(setup_test_db):
    # given: menu instance
    menu = create_menu()
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}/submenus'
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


def test_submenu_get_target_id(setup_test_db):
    # given: menu and submenu instances
    menu = create_menu()
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}/submenus/{submenu.id}'
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting status code 200 and create_menu info in response
    assert response.status_code == 200
    assert response.json()['title'] == "testSubMenu1"
    assert response.json()['description'] == "testSubMenu1Description"
    assert response.json()['id'] == submenu.id


def test_submenu_patch_target_id(setup_test_db):
    # given: menu and submenu instances
    menu = create_menu()
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}/submenus/{submenu.id}'
    # when: executing CRUD operation patch
    patch_data = {
        'description': 'patchedSubMenuDescriptionData1'
    }
    response = client.patch(url, json=patch_data)
    # then: expecting status code 200 and patched info in response
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedSubMenuDescriptionData1'
    assert response.json()['title'] != 'patchedSubMenuData1'


def test_submenu_delete_taget_id(setup_test_db):
    # given: menu and submenu instances
    menu = create_menu()
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = f'/api/v1/menus/{menu.id}/submenus/{submenu.id}'
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting status code 200 
    assert response.status_code == 200 
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting status code 404 and not found details
    assert response.status_code == 404
    assert response.json() == {"detail":"submenu not found"}


# unit testing CRUD for dishes endpoints
def test_dish_get_list(setup_test_db):
    # given: available menu and submenu
    menu = create_menu()
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() == []


def test_dish_get_list_with_data_in_db(setup_test_db):
    # given: available menu, submenu and dish
    menu = create_menu()
    submenu = create_submenu(menu.id)
    create_dish(submenu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() != []


def test_dish_post(setup_test_db):
    # given: available menu and submenu
    menu = create_menu()
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
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


def test_dish_get_target_id(setup_test_db):
    # given: available menu, submenu and dish
    menu = create_menu()
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting to get 200 and available instance data in response
    assert response.status_code == 200
    assert response.json()['id'] == dish.id
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '11.10'


def test_dish_update_target_id(setup_test_db):
    # given: available menu, submenu and dish
    menu = create_menu()
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
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


def test_dish_delete_target_id(setup_test_db):
    # given: available menu, submenu and dish
    menu = create_menu()
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting to get 404 status code and not found message
    assert response.status_code == 404
    assert response.json() == {"detail":"dish not found"}

