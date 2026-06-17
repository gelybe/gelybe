from typing import AsyncGenerator

import pytest
import pytest_asyncio
from database import engine, get_db
from fastapi.testclient import TestClient
from main import app
from models import Base, Recipe
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="session")
async def setup_database() -> AsyncGenerator[None, None]:
    """
    Фикстура для настройки базы данных перед тестами.
    Создает таблицы и очищает их после тестов.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура для создания сессии базы данных для каждого теста.
    """
    async with AsyncSession(engine) as session:
        # Очищаем базу данных перед каждым тестом
        await session.execute(text("DELETE FROM recipes"))
        await session.commit()
        yield session

@pytest.fixture
def client() -> TestClient:
    """
    Фикстура для создания тестового клиента для тестирования API.
    """
    with TestClient(app) as test_client:
        yield test_client

def test_get_recipes_empty(db_session, client):
    """
    Тест получения списка рецептов, когда база пуста.
    """
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []

def test_create_recipe(db_session, client):
    """
    Тест создания нового рецепта.
    """
    recipe_data = {
        "name": "Борщ",
        "cooking_time": 60,
        "ingredients": ["свекла", "картофель", "морковь"],
        "description": "Классический украинский борщ."
    }
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Борщ"
    assert data["views"] == 0
    assert data["cooking_time"] == 60
    assert data["ingredients"] == ["свекла", "картофель", "морковь"]
    assert data["description"] == "Классический украинский борщ."
    assert "id" in data

def test_get_recipe_detail(db_session, client):
    """
    Тест получения детальной информации о рецепте и увеличения просмотров.
    """
    # Сначала создаем рецепт
    recipe_data = {
        "name": "Паста",
        "cooking_time": 20,
        "ingredients": ["макароны", "соус"],
        "description": "Простая паста."
    }
    create_response = client.post("/recipes", json=recipe_data)
    recipe_id = create_response.json()["id"]

    # Получаем детали рецепта (должен увеличить views)
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Паста"
    assert data["views"] == 1  # views увеличился

    # Повторный запрос должен увеличить views до 2
    response2 = client.get(f"/recipes/{recipe_id}")
    data2 = response2.json()
    assert data2["views"] == 2

def test_get_recipe_not_found(client):
    """
    Тест получения несуществующего рецепта.
    """
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Рецепт не найден"}

def test_get_recipes_sorted(db_session, client):
    """
    Тест сортировки рецептов по просмотрам и времени приготовления.
    """
    # Создаем рецепты с разными views и cooking_time
    recipes = [
        {"name": "Рецепт1", "cooking_time": 30, "ingredients": ["инг1"], "description": "desc1"},
        {"name": "Рецепт2", "cooking_time": 20, "ingredients": ["инг2"], "description": "desc2"},
        {"name": "Рецепт3", "cooking_time": 40, "ingredients": ["инг3"], "description": "desc3"},
    ]
    ids = []
    for r in recipes:
        resp = client.post("/recipes", json=r)
        ids.append(resp.json()["id"])

    # Просматриваем рецепты, чтобы установить views
    client.get(f"/recipes/{ids[0]}")  # views=1
    client.get(f"/recipes/{ids[1]}")  # views=1
    client.get(f"/recipes/{ids[1]}")  # views=2
    client.get(f"/recipes/{ids[2]}")  # views=1

    # Получаем список и проверяем сортировку
    response = client.get("/recipes")
    data = response.json()
    assert len(data) == 3
    # Сортировка: сначала по views desc, затем по cooking_time asc
    # Рецепт2 (views=2, cooking_time=20), Рецепт1 (views=1, cooking_time=30), Рецепт3 (views=1, cooking_time=40)
    assert data[0]["name"] == "Рецепт2"
    assert data[1]["name"] == "Рецепт1"
    assert data[2]["name"] == "Рецепт3"
