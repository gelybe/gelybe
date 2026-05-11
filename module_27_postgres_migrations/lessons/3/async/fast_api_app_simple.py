import uvicorn
from fastapi import FastAPI
from typing import Dict, Any, List
from contextlib import asynccontextmanager
from pydantic import BaseModel

# Модели данных для демонстрации
class User(BaseModel):
    id: int
    name: str
    surname: str = None

class Product(BaseModel):
    id: int
    title: str
    count: int = 0
    price: float = 0
    user_id: int

# Временное хранилище данных в памяти
users_db = [
    {"id": 1, "name": "u1", "surname": None},
    {"id": 2, "name": "u2", "surname": None},
    {"id": 3, "name": "u3", "surname": None}
]

products_db = [
    {"id": 1, "title": "p1", "count": 0, "price": 0, "user_id": 1},
    {"id": 2, "title": "p2", "count": 0, "price": 0, "user_id": 2},
    {"id": 3, "title": "p3", "count": 0, "price": 0, "user_id": 3}
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Приложение запускается...")
    print(f"Загружено {len(users_db)} пользователей и {len(products_db)} продуктов")
    
    yield
    
    # Shutdown
    print("Приложение останавливается...")

app = FastAPI(
    title="Demo API",
    description="Демонстрационное FastAPI приложение без PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

@app.get('/')
async def root():
    return {"message": "Добро пожаловать в демонстрационное FastAPI приложение!"}

@app.get('/products')
async def get_products_handler():
    """Получить список всех продуктов с информацией о пользователях"""
    products_list = []
    for product in products_db:
        product_obj = product.copy()
        # Найти пользователя для продукта
        user = next((u for u in users_db if u["id"] == product["user_id"]), None)
        product_obj['user'] = user
        products_list.append(product_obj)
    
    return products_list

@app.get('/products/{product_id}')
async def get_product_handler(product_id: int):
    """Получить продукт по ID"""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    product_obj = product.copy()
    user = next((u for u in users_db if u["id"] == product["user_id"]), None)
    product_obj['user'] = user
    
    return product_obj

@app.post('/products', status_code=201)
async def insert_product_handler(product: Product):
    """Добавить новый продукт"""
    new_id = max(p["id"] for p in products_db) + 1 if products_db else 1
    new_product = {
        "id": new_id,
        "title": product.title,
        "count": product.count,
        "price": product.price,
        "user_id": product.user_id
    }
    products_db.append(new_product)
    return new_product

@app.delete('/products/{product_id}', status_code=202)
async def delete_product_handler(product_id: int):
    """Удалить продукт по ID"""
    product_index = next((i for i, p in enumerate(products_db) if p["id"] == product_id), None)
    if product_index is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    deleted_product = products_db.pop(product_index)
    return {"message": f"Продукт '{deleted_product['title']}' удален"}

@app.get('/users')
async def get_users_handler():
    """Получить список всех пользователей"""
    return users_db

@app.get('/users/{user_id}')
async def get_user_handler(user_id: int):
    """Получить пользователя по ID"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

if __name__ == '__main__':
    uvicorn.run("fast_api_app_simple:app", port=1111, host='127.0.0.1', reload=True)
