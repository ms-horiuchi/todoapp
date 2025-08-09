from pydantic import BaseModel, Field
from datetime import datetime

class Item(BaseModel):
    item_id: int | None = Field(default=None, title="アイテムID", description="一意なアイテムID（自動生成）")
    task_name: str = Field(..., title="タスク名", description="アイテムのタスク名", max_length=100)
    user_id: str = Field(..., title="ユーザID", description="このアイテムを所有するユーザのID", max_length=20)
    expire_date: datetime = Field(..., title="期限日", description="アイテムの期限日")
    finished_date: datetime | None = Field(default=None, title="完了日", description="アイテムの完了日")
    
    class Config:
        from_attributes = True
