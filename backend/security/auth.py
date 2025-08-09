from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import jwt  # ここを修正
from datetime import datetime, timedelta
from cruds.user import get_user_by_id
from tododb import get_db_session

security = HTTPBearer()
SECRET_KEY = "learning-secret-key"
ALGORITHM = "HS256"

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # jwt.encode

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_db_session)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])  # jwt.decode
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="無効なトークン")
        
        user = await get_user_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="ユーザーが見つかりません")
        
        return user
    except jwt.ExpiredSignatureError:  # jwt.ExpiredSignatureError
        raise HTTPException(status_code=401, detail="トークンの有効期限が切れています")
    except jwt.JWTError:  # jwt.JWTError
        raise HTTPException(status_code=401, detail="無効なトークン")