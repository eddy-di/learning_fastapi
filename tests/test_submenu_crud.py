from app.routers.submenu import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
    update_submenu,
)
from app.utils.pathfinder import reverse


# testing CRUD for submenus endpoints
def test_submenu_get_list(setup_test_db, create_menu):
    # given: menu instance
    menu = create_menu
    client = setup_test_db
    url = reverse(get_submenus, target_menu_id=menu.id)
    # when: executing CRUD operation get on list
    response = client.get(url)
    # then: expecting status code 200 and empty list in response
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_get_list_with_data_in_db(setup_test_db, create_menu, create_submenu, create_dish):
    # given: an instance of menu, submenu and dish objs
    client = setup_test_db
    menu = create_menu
    submenu = create_submenu(menu.id)
    create_dish(submenu.id)
    # when: executing CRUD operation get on menus list
    url = reverse(get_submenus, target_menu_id=menu.id)
    response = client.get(url)
    # then: expecting to get status code 200 and data on available instances of each objects
    assert response.status_code == 200
    assert response.json()[0]['id'] == submenu.id
    assert response.json()[0]['title'] == 'testSubMenu1'
    assert response.json()[0]['description'] == 'testSubMenu1Description'
    assert response.json()[0]['dishes_count'] == 1


def test_submenu_post(setup_test_db, create_menu):
    # given: menu instance
    menu = create_menu
    client = setup_test_db
    url = reverse(create_submenu, target_menu_id=menu.id)
    # when: executing CRUD operation post
    post_data = {
        'title': 'subMenuTitle1',
        'description': 'subMenuDescription1'
    }
    response = client.post(url, json=post_data)
    # then: expecting status code 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'subMenuTitle1'
    assert response.json()['description'] == 'subMenuDescription1'


def test_submenu_get_target_id(setup_test_db, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = reverse(get_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on target id
    response = client.get(url)
    # then: expecting status code 200 and create_menu info in response
    assert response.status_code == 200
    assert response.json()['title'] == 'testSubMenu1'
    assert response.json()['description'] == 'testSubMenu1Description'
    assert response.json()['id'] == submenu.id


def test_submenu_patch_target_id(setup_test_db, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = reverse(update_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation patch
    patch_data = {
        'description': 'patchedSubMenuDescriptionData1'
    }
    response = client.patch(url, json=patch_data)
    # then: expecting status code 200 and patched info in response
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedSubMenuDescriptionData1'
    assert response.json()['title'] != 'patchedSubMenuData1'


def test_submenu_delete_taget_id(setup_test_db, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = create_submenu(menu.id)
    client = setup_test_db
    url = reverse(delete_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation delete
    response = client.delete(url)
    # then: expecting status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get
    response = client.get(url)
    # then: expecting status code 404 and not found details
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
