import pytest
from httpx import AsyncClient

from app.routers.menu import get_menus_preview
from app.utils.pathfinder import reverse


@pytest.mark.asyncio
async def test_empty_menu_preview(async_client: AsyncClient):

    url = reverse(get_menus_preview)

    response = await async_client.get(url)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_menu_preview_with_menu(async_client: AsyncClient, create_menu):

    url = reverse(get_menus_preview)

    response = await async_client.get(url)

    assert response.status_code == 200
    assert response.json() != []
    assert response.json()[0]['id'] == create_menu.id
    assert response.json()[0]['title'] == create_menu.title
    assert response.json()[0]['description'] == create_menu.description
