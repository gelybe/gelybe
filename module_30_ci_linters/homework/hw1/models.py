from typing import List

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    """
    Модель рецепта в базе данных.

    Attributes:
        id (int): Уникальный идентификатор рецепта (автоинкремент).
        name (str): Название блюда.
        views (int): Количество просмотров рецепта (по умолчанию 0).
        cooking_time (int): Время приготовления в минутах.
        ingredients (list): Список ингредиентов (хранится как JSON).
        description (str): Текстовое описание рецепта.
    """

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
