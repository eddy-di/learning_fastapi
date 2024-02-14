import pytest
from httpx import AsyncClient

from app.routers.menu import get_menus_preview
from app.utils.pathfinder import reverse


@pytest.mark.asyncio
async def test_empty_menu_preview(async_client: AsyncClient):
    # given: empty database
    url = reverse(get_menus_preview)
    # when: executing GET operation on endpoint
    response = await async_client.get(url)
    # then: expecting it to return empty list
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_menu_preview_with_menu(async_client: AsyncClient, create_menu):
    # given: a db with menu instance
    url = reverse(get_menus_preview)
    # when: executing GET operation on endpoint
    response = await async_client.get(url)
    # then: expecting it to return menu instance
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()[0]['id'] == create_menu.id
    assert response.json()[0]['title'] == create_menu.title
    assert response.json()[0]['description'] == create_menu.description
