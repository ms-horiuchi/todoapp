from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """標準APIレスポンス"""
    success: bool = True
    message: str
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    success: bool = False
    message: str
    error_code: Optional[str] = None

class LoginResponse(BaseModel):
    """ログインレスポンス"""
    access_token: str
    token_type: str = "bearer"
    user: dict