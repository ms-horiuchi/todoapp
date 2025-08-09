from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from tododb import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "todo_item"

    item_id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_name: str = Column(String(100), nullable=False)
    user_id: str =  Column(String(20), ForeignKey('todo_user.user_id', ondelete='SET NULL'), nullable=False)
    expire_date: datetime = Column(DateTime, nullable=False)
    finished_date: datetime = Column(DateTime, nullable=True)

    # リレーションシップの定義
    user = relationship("User", back_populates="items")
