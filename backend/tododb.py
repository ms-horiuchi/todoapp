import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(os.path.dirname(__file__), 'tododb.sqlite')

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db_session():
    async with async_session() as session:
        yield session   


