import os
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from models.user import User  # Userモデルをインポート
from models.item import Item  # Itemモデルをインポート
from tododb import Base

base_dir = os.path.dirname(__file__)

DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(base_dir, 'tododb.sqlite')

engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    print("=== データベースの初期化を開始 ===")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("=== データベースの初期化が完了 ===")

if __name__ == "__main__":
    asyncio.run(init_db())
    print("データベースの初期化が完了しました。")
