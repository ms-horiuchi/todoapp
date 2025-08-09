from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: str = Field(..., title="ユーザID", description="一意なユーザID", max_length=20)
    name: str = Field(..., title="ユーザ名", description="ユーザの名前", max_length=40)
    password: str = Field(..., title="パスワード", description="ユーザのパスワード", max_length=100)

    class Config:
        from_attributes = True
