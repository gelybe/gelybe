from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase


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

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    views = Column(Integer, default=0)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(JSON, nullable=False)
    description = Column(Text, nullable=False)
