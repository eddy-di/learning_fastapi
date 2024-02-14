import pytest
from httpx import AsyncClient

from app.routers.dish import create_dish, delete_dish, get_dish, get_dishes, update_dish
from app.utils.generators import generate_uuid
from app.utils.pathfinder import reverse


# unit testing CRUD for dishes endpoints
@pytest.mark.asyncio
async def test_dish_get_list(async_client: AsyncClient, create_menu, create_submenu):
    # given: available menu and submenu
    menu = create_menu
    submenu = await create_submenu(menu.id)
    url = reverse(get_dishes, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on list
    response = await async_client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_dish_get_list_with_data_in_db(async_client: AsyncClient, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = await create_submenu(menu.id)
    await create_dish(submenu.id)
    url = reverse(get_dishes, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on list
    response = await async_client.get(url)
    # then: expecting to get 200 and empty list
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_dish_post(async_client: AsyncClient, create_menu, create_submenu):
    # given: available menu and submenu
    menu = create_menu
    submenu = await create_submenu(menu.id)
    url = reverse(create_dish, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation post
    post_data = {
        'id': generate_uuid(),
        'title': 'testDishTitle1',
        'description': 'testDishDescription1',
        'price': '12.12'
    }
    response = await async_client.post(url, json=post_data)
    # then: expecting to get 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '12.12'


@pytest.mark.asyncio
async def test_dish_get_target_id(async_client: AsyncClient, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = await create_submenu(menu.id)
    dish = await create_dish(submenu.id)
    url = reverse(get_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
    # when: executing CRUD operation get on target id
    response = await async_client.get(url)
    # then: expecting to get 200 and available instance data in response
    assert response.status_code == 200
    assert response.json()['id'] == dish.id
    assert response.json()['title'] == 'testDishTitle1'
    assert response.json()['description'] == 'testDishDescription1'
    assert response.json()['price'] == '11.10'


@pytest.mark.asyncio
async def test_dish_update_target_id(async_client: AsyncClient, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = await create_submenu(menu.id)
    dish = await create_dish(submenu.id)
    url = reverse(update_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
    # when: executing CRUD operation patch
    patch_data = {
        'price': '33.99'
    }
    response = await async_client.patch(url, json=patch_data)
    # then: expecting to get 200 and changed field in response
    assert response.status_code == 200
    assert response.json()['price'] == '33.99'
    assert response.json()['title'] != '33.99'
    assert response.json()['description'] != '33.99'


@pytest.mark.asyncio
async def test_dish_delete_target_id(async_client: AsyncClient, create_menu, create_submenu, create_dish):
    # given: available menu, submenu and dish
    menu = create_menu
    submenu = await create_submenu(menu.id)
    dish = await create_dish(submenu.id)
    url = reverse(delete_dish, target_menu_id=menu.id, target_submenu_id=submenu.id, target_dish_id=dish.id)
    # when: executing CRUD operation delete
    response = await async_client.delete(url)
    # then: expecting to get status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get
    response = await async_client.get(url)
    # then: expecting to get 404 status code and not found message
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}
