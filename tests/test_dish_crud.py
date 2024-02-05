from app.routers.dish import (
    create_dish,
    delete_dish,
    read_dish,
    read_dishes,
    update_dish,
)
from app.utils.pathfinder import reverse


# unit testing CRUD for dishes endpoints
def test_dish_get_list(setup_test_db, create_menu, create_submenu):
    # given: available menu and submenu
    menu = create_menu
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = reverse(read_dishes, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() == []


def test_dish_get_list_with_data_in_db(setup_test_db, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = create_submenu(menu.id)
    create_dish(submenu.id)
    client = setup_test_db
    url = reverse(read_dishes, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() != []


def test_dish_post(setup_test_db, create_menu, create_submenu):
    # given: available menu and submenu
    menu = create_menu
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = reverse(create_dish, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation post
    post_data = {
        'title': 'testDishTitle1',
        'description': 'testDishDescription1',
        'price': '12.12'
    }
    response = client.post(url, json=post_data)
    # then: expecting to get 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '12.12'


def test_dish_get_target_id(setup_test_db, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = reverse(read_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting to get 200 and available instance data in response
    assert response.status_code == 200
    assert response.json()['id'] == dish.id
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '11.10'


def test_dish_update_target_id(setup_test_db, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = reverse(update_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
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


def test_dish_delete_target_id(setup_test_db, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = create_submenu(menu.id)
    dish = create_dish(submenu.id)
    client = setup_test_db
    url = reverse(delete_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting to get 404 status code and not found message
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}
