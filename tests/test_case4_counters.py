import uuid

import pytest
from httpx import AsyncClient

from app.routers.dish import create_dish, get_dishes
from app.routers.menu import create_menu, delete_menu, get_menu, get_menus
from app.routers.submenu import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
)
from app.utils.pathfinder import reverse

menu_id = None
submenu_id = None
dish1_id = None
dish2_id = None


@pytest.mark.asyncio
async def test_create_menu(scenario_client: AsyncClient,):
    # given: empty db with initialized tables
    global menu_id
    url = reverse(create_menu)
    # when: executing POST operation for menu instance
    data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = await scenario_client.post(url, json=data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My menu 1'
    assert response.json()['description'] == 'My menu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    menu_id = response.json()['id']


@pytest.mark.asyncio
async def test_submenu_create(scenario_client: AsyncClient,):
    # given: menu instance
    global menu_id
    global submenu_id
    submenus_url = reverse(create_submenu, target_menu_id=menu_id)
    # when: executing POST operation for submenu instance
    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': menu_id
    }
    response = await scenario_client.post(submenus_url, json=submenu_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My submenu 1'
    assert response.json()['description'] == 'My submenu description 1'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    submenu_id = response.json()['id']


@pytest.mark.asyncio
async def test_dish_create_case1(scenario_client: AsyncClient,):
    # given: menu and linked submenu instance
    global menu_id
    global submenu_id
    global dish1_id
    dish_url = reverse(create_dish, target_menu_id=menu_id, target_submenu_id=submenu_id)
    # when: executing POST operation for first dish instance
    dish1_data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    response = await scenario_client.post(dish_url, json=dish1_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 2'
    assert response.json()['description'] == 'My dish description 2'
    assert response.json()['price'] == '13.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish1_id = response.json()['id']


@pytest.mark.asyncio
async def test_dish_create_case2(scenario_client: AsyncClient,):
    # given: menu and linked submenu instance
    global menu_id
    global submenu_id
    global dish2_id
    dish_url = reverse(create_dish, target_menu_id=menu_id, target_submenu_id=submenu_id)
    # when: executing POST operation for second dish instance
    dish2_data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = await scenario_client.post(dish_url, json=dish2_data)
    # then: expecting to get passed data in response, save generated id in global variable
    assert response.status_code == 201
    assert response.json()['title'] == 'My dish 1'
    assert response.json()['description'] == 'My dish description 1'
    assert response.json()['price'] == '12.50'
    assert isinstance(uuid.UUID(response.json()['id'], version=4), uuid.UUID)

    dish2_id = response.json()['id']


@pytest.mark.asyncio
async def test_get_counters_for_target_menu(scenario_client: AsyncClient,):
    # given: menu linked with submenu and two dish instances
    global menu_id
    url = reverse(get_menu, target_menu_id=menu_id)
    # when: executing GET operation for target menu
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and submenus_count == 1, dishes_count == 2
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == menu_id


@pytest.mark.asyncio
async def test_get_counters_for_target_submenu(scenario_client: AsyncClient,):
    # given: menu linked with submenu and two dish instances
    global menu_id
    global submenu_id
    url = reverse(get_submenu, target_menu_id=menu_id, target_submenu_id=submenu_id)
    # when: executing GET operation for target submenu
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and dishes_count == 2
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 2
    assert response.json()['id'] == submenu_id


@pytest.mark.asyncio
async def test_delete_target_submenu(scenario_client: AsyncClient,):
    # given: menu linked with submenu and two dish instances
    global menu_id
    global submenu_id
    url = reverse(delete_submenu, target_menu_id=menu_id, target_submenu_id=submenu_id)
    # when: executing DELETE operation for target submenu
    response = await scenario_client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_submenu_list(scenario_client: AsyncClient,):
    # given: menu instance
    global menu_id
    url = reverse(get_submenus, target_menu_id=menu_id)
    # when: executing GET operation for submenu list
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and empty submenus
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_dishes_list(scenario_client: AsyncClient,):
    # given: menu instance
    global menu_id
    global submenu_id
    url = reverse(get_dishes, target_menu_id=menu_id, target_submenu_id=submenu_id)
    # when: executing GET operation for dishes list
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and empty dishes
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_target_menu(scenario_client: AsyncClient,):
    # given: menu instance
    global menu_id
    url = reverse(get_menu, target_menu_id=menu_id)
    # when: executing GET operation for target menu
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and submenus_count == 0, dishes_count == 0
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0
    assert response.json()['id'] == menu_id


@pytest.mark.asyncio
async def test_delete_target_menu(scenario_client: AsyncClient,):
    # given: menu instance
    global menu_id
    url = reverse(delete_menu, target_menu_id=menu_id)
    # when: executing DELETE operation for target menu
    response = await scenario_client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_menus_list(scenario_client: AsyncClient,):
    # given: empty db
    url = reverse(get_menus)
    # when: executing GET operation for menu list
    response = await scenario_client.get(url)
    # then: expecting to get status code 200 and empty menus
    assert response.status_code == 200
    assert response.json() == []
