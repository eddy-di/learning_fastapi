from fastapi.testclient import TestClient
import uuid
from database import TestingRUDSessionLocal
from models import Menu, SubMenu

from main import app

client = TestClient(app)

def create_menu(id: str):
    session = TestingRUDSessionLocal()
    db_menu_item = Menu(
        id=id, 
        title='testMenu1', 
        description='testMenu1Description'
    )
    session.add(db_menu_item)
    session.commit()
    session.close()

def test_submenu_get_list(test_db):
    # given: menu instance and url
    id = str(uuid.uuid4)
    create_menu(id)
    url = f'/api/v1/menus/{id}/submenus'
    # when: accessing the endpoint
    response = client.get(url)
    # then: expeting to get empty list and code 200
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_post(test_db):
    # given: menu instance and url
    id = str(uuid.uuid4)
    create_menu(id)
    url = f'/api/v1/menus/{id}/submenus'
    # when:
    post_data = {
        "title": "subMenuTitle1",
        "description": "subMenuDescription1"
    }
    response = client.post(url, json=post_data)
    content = response.content.decode('utf-8')
    print(content)
    # then:
    assert response.status_code == 201
    assert response.json()['title'] == 'subMenuTitle1'
    assert response.json()['description'] == 'subMenuDescription1'










    # given:

    # when:

    # then:
    # content = response.content.decode('utf-8')