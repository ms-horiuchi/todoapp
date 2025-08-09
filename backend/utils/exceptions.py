from fastapi import HTTPException

class TodoAppException(Exception):
    """アプリケーション固有の例外基底クラス"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(TodoAppException):
    def __init__(self, resource: str = "リソース"):
        super().__init__(f"{resource}が見つかりません", 404)

class AuthenticationError(TodoAppException):
    def __init__(self, message: str = "認証に失敗しました"):
        super().__init__(message, 401)

class ValidationError(TodoAppException):
    def __init__(self, message: str = "入力データが無効です"):
        super().__init__(message, 400)

def raise_not_found(resource: str = "リソース"):
    """404エラーを発生させる共通関数"""
    raise HTTPException(status_code=404, detail=f"{resource}が見つかりません")

def raise_bad_request(message: str = "リクエストが無効です"):
    """400エラーを発生させる共通関数"""
    raise HTTPException(status_code=400, detail=message)