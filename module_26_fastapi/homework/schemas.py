from pydantic import BaseModel
from typing import List

class RecipeList(BaseModel):
    """
    Схема для списка рецептов (GET /recipes).
    Используется для отображения в таблице: название, просмотры, время приготовления.

    Attributes:
        id (int): Уникальный идентификатор рецепта.
        name (str): Название блюда.
        views (int): Количество просмотров рецепта.
        cooking_time (int): Время приготовления в минутах.
    """
    id: int
    name: str
    views: int
    cooking_time: int

class RecipeCreate(BaseModel):
    """
    Схема для создания нового рецепта (POST /recipes).
    Содержит все необходимые поля для создания рецепта.

    Attributes:
        name (str): Название блюда.
        cooking_time (int): Время приготовления в минутах.
        ingredients (List[str]): Список ингредиентов.
        description (str): Текстовое описание рецепта.
    """
    name: str
    cooking_time: int
    ingredients: List[str]
    description: str

class RecipeDetail(BaseModel):
    """
    Схема для детальной информации о рецепте (GET /recipes/{id}, POST /recipes).
    Включает все поля рецепта, включая ингредиенты и описание.

    Attributes:
        id (int): Уникальный идентификатор рецепта.
        name (str): Название блюда.
        cooking_time (int): Время приготовления в минутах.
        ingredients (List[str]): Список ингредиентов.
        description (str): Текстовое описание рецепта.
        views (int): Количество просмотров рецепта.
    """
    id: int
    name: str
    cooking_time: int
    ingredients: List[str]
    description: str
    views: int
