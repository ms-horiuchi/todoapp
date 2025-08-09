from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.item import Item as ItemModel
from schemas.item import Item as ItemSchema
from datetime import datetime

async def get_item(session: AsyncSession) -> list[ItemSchema]:
    """
    全タスクを取得する関数
    """
    try:
        result = await session.execute(select(ItemModel))
        items = result.scalars().all()
        return [ItemSchema.model_validate(item) for item in items]
    except Exception as e:
        print(f"Error occurred while fetching items: {e}")
        return []

async def get_item_by_user_id(session: AsyncSession, user_id: int) -> list[ItemSchema]:
    """
    ユーザーIDに紐づく全タスクを取得する関数
    """
    try:
        result = await session.execute(select(ItemModel).where(ItemModel.user_id == user_id))
        items = result.scalars().all()
        return [ItemSchema.model_validate(item) for item in items]
    except Exception as e:
        print(f"Error occurred while fetching items: {e}")
        return []
    
async def get_item_by_id(session: AsyncSession, item_id: int) -> ItemSchema | None:
    """
    タスクIDでタスク情報を取得する関数
    
    Args:
        session (AsyncSession): 非同期データベースセッション
        item_id (str): 検索対象のタスクID

    Returns:
        ItemSchema | None: 
            - タスクが存在する場合: タスク情報のPydanticモデル
            - タスクが存在しない場合: None
    """
    try:
        result = await session.execute(
            select(ItemModel).where(ItemModel.item_id == item_id)
        )
        item = result.scalar_one_or_none()
        return ItemSchema.model_validate(item) if item else None
    except Exception as e:
        print(f"Error occurred while fetching item by id: {e}")
        return None

async def delete_item(session: AsyncSession, item_id: int) -> bool:
    """
    タスクIDでタスクを削除する関数

    Args:
        session (AsyncSession): 非同期データベースセッション
        id (str): 削除対象のタスクID
        
    Returns:
        bool: 削除成功時True、失敗時False
    """
    try:
        result = await session.execute(
            select(ItemModel).where(ItemModel.item_id == item_id)
        )
        item = result.scalar_one_or_none()
        if item:
            await session.delete(item)
            await session.commit()
            return True
        return False
    except Exception as e:
        await session.rollback()
        print(f"Error occurred while deleting item: {e}")
        return False

async def create_item(session: AsyncSession, item: ItemSchema) -> ItemSchema | None:
    """
    タスクを新規作成する関数

    Args:
        session (AsyncSession): 非同期データベースセッション
        item (ItemSchema): 作成するタスクの情報

    Returns:
        ItemSchema | None: 作成されたタスクの情報またはNone
    """
    try:
        # Pydanticモデルから辞書に変換してSQLAlchemyモデルを作成
        new_item = ItemModel(**item.model_dump(exclude_unset=True))
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        # SQLAlchemyモデルをPydanticモデルに変換して返す
        return ItemSchema.model_validate(new_item)
    except Exception as e:
        await session.rollback()
        print(f"Error occurred while creating item: {e}")
        return None

async def update_item(session: AsyncSession, item_id: int, item_data: ItemSchema) -> ItemSchema | None:
    """
    タスクを更新する関数

    Args:
        session (AsyncSession): 非同期データベースセッション
        item_id (str): 更新対象のタスクID
        item_data (ItemSchema): 更新するタスクの情報

    Returns:
        ItemSchema | None: 
            - 更新成功: 更新後のタスク情報
            - タスクが存在しない場合: None
    """
    try:
        result = await session.execute(
            select(ItemModel).where(ItemModel.item_id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
            
        # Pydanticの自動変換を活用してシンプルに更新
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
            
        await session.commit()
        await session.refresh(item)
        return ItemSchema.model_validate(item)
        
    except Exception as e:
        await session.rollback()
        print(f"Error occurred while updating item: {e}")
        return None

async def update_finished_date(session: AsyncSession, item_id: int, finished_date: datetime | None) -> ItemSchema | None:
    """
    タスクの完了日を更新する関数

    Args:
        session (AsyncSession): 非同期データベースセッション
        item_id (str): 更新対象のタスクID
        finished_date (datetime | None): 新しい完了日（Noneで未完了に戻す）

    Returns:
        ItemSchema | None: 
            - 更新成功: 更新後のタスク情報
            - タスクが存在しない場合: None
    """
    try:
        result = await session.execute(
            select(ItemModel).where(ItemModel.item_id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
            
        item.finished_date = finished_date
        await session.commit()
        await session.refresh(item)
        return ItemSchema.model_validate(item)
        
    except Exception as e:
        await session.rollback()
        print(f"Error occurred while updating finish date: {e}")
        return None