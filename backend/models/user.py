from sqlalchemy import Column, Integer, String, DateTime
from tododb import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "todo_user"

    user_id: str = Column(String(20), primary_key=True)
    name: str = Column(String(40), nullable=False)
    password: str = Column(String(100), nullable=False)
    # リレーションシップの定義
    items = relationship("Item", back_populates="user")