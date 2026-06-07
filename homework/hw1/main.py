from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import uvicorn
from contextlib import asynccontextmanager
from typing import List

from database import get_db, engine
from models import Base, Recipe
from schemas import RecipeCreate, RecipeList, RecipeDetail

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Инициализация базы данных при запуске приложения.
    Создает все таблицы, если они не существуют.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="API Кулинарной Книги",
    description="Сервис для управления рецептами. Позволяет получать список рецептов, просматривать детали и создавать новые рецепты.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/", summary="Корневой эндпоинт")
async def root() -> dict:
    """
    Возвращает приветственное сообщение и информацию о доступных эндпоинтах.
    """
    return {
        "message": "Добро пожаловать в API Кулинарной Книги!",
        "endpoints": {
            "GET /recipes": "Получить список всех рецептов",
            "GET /recipes/{recipe_id}": "Получить детальную информацию о рецепте",
            "POST /recipes": "Создать новый рецепт"
        },
        "docs": "http://localhost:5000/docs",
        "redoc": "http://localhost:5000/redoc"
    }

@app.get("/recipes", response_model=List[RecipeList], summary="Получить список всех рецептов")
async def get_recipes(db: AsyncSession = Depends(get_db)) -> List[RecipeList]:
    """
    Возвращает список всех рецептов, отсортированных по популярности (количеству просмотров) в убывающем порядке.
    Если просмотры совпадают, сортировка по времени приготовления в возрастающем порядке.

    - **Возвращает**: Список рецептов с полями id, name, views, cooking_time.
    """
    result = await db.execute(
        select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
    )
    recipes = result.scalars().all()
    return [RecipeList(id=r.id, name=r.name, views=r.views, cooking_time=r.cooking_time) for r in recipes]

@app.get("/recipes/{recipe_id}", response_model=RecipeDetail, summary="Получить детальную информацию о рецепте")
async def get_recipe_detail(recipe_id: int, db: AsyncSession = Depends(get_db)) -> RecipeDetail:
    """
    Возвращает детальную информацию о рецепте по его ID.
    При каждом просмотре количество просмотров увеличивается на 1.

    - **recipe_id**: Уникальный идентификатор рецепта.
    - **Возвращает**: Детальную информацию о рецепте, включая ingredients и description.
    - **Ошибки**: 404, если рецепт не найден.
    """
    # Получаем рецепт
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    # Увеличиваем количество просмотров
    await db.execute(
        update(Recipe).where(Recipe.id == recipe_id).values(views=recipe.views + 1)
    )
    await db.commit()

    # Возвращаем обновленную информацию
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    updated_recipe = result.scalar_one()
    return RecipeDetail(
        id=updated_recipe.id,
        name=updated_recipe.name,
        cooking_time=updated_recipe.cooking_time,
        ingredients=updated_recipe.ingredients,
        description=updated_recipe.description,
        views=updated_recipe.views,
    )

@app.post("/recipes", response_model=RecipeDetail, summary="Создать новый рецепт")
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_db)) -> RecipeDetail:
    """
    Создает новый рецепт на основе предоставленных данных.

    - **recipe**: Данные для создания рецепта (name, cooking_time, ingredients, description).
    - **Возвращает**: Созданный рецепт с присвоенным ID и views=0.
    """
    new_recipe = Recipe(
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
        views=0,
    )
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return RecipeDetail(
        id=new_recipe.id,
        name=new_recipe.name,
        cooking_time=new_recipe.cooking_time,
        ingredients=new_recipe.ingredients,
        description=new_recipe.description,
        views=new_recipe.views,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
