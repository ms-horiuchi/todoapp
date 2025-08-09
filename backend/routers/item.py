from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.item import get_item, get_item_by_id, delete_item, update_finished_date, create_item, update_item
from schemas.item import Item
from security.auth import get_current_user
from tododb import get_db_session
from datetime import datetime
from utils.exceptions import raise_not_found, raise_bad_request

router = APIRouter(tags=["Items"], prefix="/items")

@router.get("/", response_model=list[Item] | None)
async def read_items_endpoint(db_session: AsyncSession = Depends(get_db_session),
                               current_user = Depends(get_current_user)):
    return await get_item(db_session)

@router.get("/{item_id}", response_model=Item | None)
async def read_item_endpoint(item_id: int, db_session: AsyncSession = Depends(get_db_session),
                              current_user = Depends(get_current_user)):
    item = await get_item_by_id(db_session, item_id)
    if not item:
        raise_not_found("Item not found")
    return item


@router.delete("/{item_id}", response_model=dict | None)
async def delete_item_endpoint(item_id: int, db_session: AsyncSession = Depends(get_db_session),
                                   current_user = Depends(get_current_user)):
    deleted = await delete_item(db_session, item_id)
    if not deleted:
        raise_not_found("Item not found")
    return {"detail": "Item deleted successfully"}

@router.put("/{item_id}/finish", response_model=Item | None)
async def finish_item_endpoint(item_id: int, finished_date: datetime | None = None, db_session: AsyncSession = Depends(get_db_session),
                                current_user = Depends(get_current_user)):
    item = await update_finished_date(db_session, item_id, finished_date)
    if not item:
        raise_not_found("Item not found")
    return item

@router.post("/", response_model=Item | None, status_code=201)
async def create_item_endpoint(item: Item, db_session: AsyncSession = Depends(get_db_session),
                                current_user = Depends(get_current_user)):
    """
    新しいタスクを作成するエンドポイント
    """
    try:
        # ユーザーIDを現在のログインユーザーに設定
        item.user_id = current_user.user_id
        new_item = await create_item(db_session, item)
        return new_item
    except Exception as e:
        raise_bad_request("Failed to create item")

@router.put("/{item_id}", response_model=Item | None)
async def update_item_endpoint(item_id: int, item: Item, db_session: AsyncSession = Depends(get_db_session),
                                current_user = Depends(get_current_user)):
    """
    タスクを更新するエンドポイント
    """
    try:
        # ユーザーIDを現在のログインユーザーに設定
        item.user_id = current_user.user_id
        updated_item = await update_item(db_session, item_id, item)
        if not updated_item:
           raise_not_found("Item not found")
        return updated_item
    except Exception as e:
        raise_bad_request("Failed to update item")