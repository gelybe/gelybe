import uvicorn
from sqlalchemy import Column, Integer, String, Float, \
    Sequence, Identity, ForeignKey, select, update
from sqlalchemy.orm import relationship, selectinload
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Dict, Any
from contextlib import asynccontextmanager

engine = create_async_engine('sqlite+aiosqlite:///./app.db')
Base = declarative_base()
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    User(name='u1'),
                    User(name='u2'),
                    User(name='u3'),
                    Product(title="p1", user_id=1),
                    Product(title="p2", user_id=2),
                    Product(title="p3", user_id=3)
                ]
            )
            await session.commit()
    
    yield
    
    # Shutdown (cleanup if needed)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    count = Column(Integer, default=0)
    price = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="products")

    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    num = Column(Integer, nullable=True)

    def __repr__(self):
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}




@app.delete('/products/{product_id}', status_code=202)
async def delete_product_handler(product_id: int):
    async with async_session() as session:
        async with session.begin():
            q = select(Product).where(Product.id == product_id)
            result = await session.execute(q)
            product = result.scalar_one()
            await session.delete(product)
            await session.commit()


@app.post('/products', status_code=201)
async def insert_product_handler():
    async with async_session() as session:
        async with session.begin():
            p = Product(title='новый продукт')
            session.add(p)
            await session.flush()


@app.get('/products')
async def get_products_handler():
    async with async_session() as session:
        async with session.begin():
            # without user
            # q = await session.execute(select(Product))
            # withuser
            q = await session.execute(
                select(Product).options(selectinload(Product.user)))

            products = q.scalars().all()
            products_list = []
            for p in products:
                product_obj = p.to_json()
                product_obj['user'] = p.user.to_json()
                products_list.append(product_obj)
            return products_list


if __name__ == '__main__':
    uvicorn.run("fast_api_app:app", port=1111, host='127.0.0.1')
