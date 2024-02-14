import pytest
from httpx import AsyncClient

from app.routers.submenu import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
    update_submenu,
)
from app.utils.pathfinder import reverse


# testing CRUD for submenus endpoints
@pytest.mark.asyncio
async def test_submenu_get_list(async_client: AsyncClient, create_menu):
    # given: menu instance
    menu = create_menu
    url = reverse(get_submenus, target_menu_id=menu.id)
    # when: executing CRUD operation get on list
    response = await async_client.get(url)
    # then: expecting status code 200 and empty list in response
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_submenu_get_list_with_data_in_db(async_client: AsyncClient, create_menu, create_submenu, create_dish):
    # given: an instance of menu, submenu and dish objs
    menu = create_menu
    submenu = await create_submenu(menu.id)
    await create_dish(submenu.id)
    # when: executing CRUD operation get on menus list
    url = reverse(get_submenus, target_menu_id=menu.id)
    response = await async_client.get(url)
    # then: expecting to get status code 200 and data on available instances of each objects
    assert response.status_code == 200
    assert response.json()[0]['id'] == submenu.id
    assert response.json()[0]['title'] == 'testSubMenu1'
    assert response.json()[0]['description'] == 'testSubMenu1Description'
    assert response.json()[0]['dishes_count'] == 1


@pytest.mark.asyncio
async def test_submenu_post(async_client: AsyncClient, create_menu):
    # given: menu instance
    menu = create_menu
    url = reverse(create_submenu, target_menu_id=menu.id)
    # when: executing CRUD operation post
    post_data = {
        'title': 'subMenuTitle1',
        'description': 'subMenuDescription1'
    }
    response = await async_client.post(url, json=post_data)
    # then: expecting status code 201 and post_data in response
    assert response.status_code == 201
    assert response.json()['title'] == 'subMenuTitle1'
    assert response.json()['description'] == 'subMenuDescription1'


@pytest.mark.asyncio
async def test_submenu_get_target_id(async_client: AsyncClient, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = await create_submenu(menu.id)
    url = reverse(get_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation get on target id
    response = await async_client.get(url)
    # then: expecting status code 200 and create_menu info in response
    assert response.status_code == 200
    assert response.json()['title'] == 'testSubMenu1'
    assert response.json()['description'] == 'testSubMenu1Description'
    assert response.json()['id'] == submenu.id


@pytest.mark.asyncio
async def test_submenu_patch_target_id(async_client: AsyncClient, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = await create_submenu(menu.id)
    url = reverse(update_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation patch
    patch_data = {
        'description': 'patchedSubMenuDescriptionData1'
    }
    response = await async_client.patch(url, json=patch_data)
    # then: expecting status code 200 and patched info in response
    assert response.status_code == 200
    assert response.json()['description'] == 'patchedSubMenuDescriptionData1'
    assert response.json()['title'] != 'patchedSubMenuData1'


@pytest.mark.asyncio
async def test_submenu_delete_taget_id(async_client: AsyncClient, create_menu, create_submenu):
    # given: menu and submenu instances
    menu = create_menu
    submenu = await create_submenu(menu.id)
    url = reverse(delete_submenu, target_menu_id=menu.id, target_submenu_id=submenu.id)
    # when: executing CRUD operation delete
    response = await async_client.delete(url)
    # then: expecting status code 200
    assert response.status_code == 200
    # when: executing CRUD operation get
    response = await async_client.get(url)
    # then: expecting status code 404 and not found details
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
