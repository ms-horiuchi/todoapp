from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.user import get_user_by_id_and_password, get_user_by_id, create_user, update_user, delete_user, get_users
from schemas.user import User as UserSchema
from security.auth import create_access_token, get_current_user
from tododb import get_db_session
from schemas.response import APIResponse
from utils.exceptions import raise_not_found, raise_bad_request
from schemas.user import User as UserSchema

router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/", response_model=APIResponse[list[UserSchema]])
async def read_users_endpoint(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    users = await get_users(db_session)
    return APIResponse(
        message="ユーザー一覧を取得しました",
        data=users
    )


@router.get("/{user_id}", response_model=APIResponse[UserSchema])
async def read_user_by_id_endpoint(
    user_id: str, db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    user = await get_user_by_id(db_session, user_id)
    if not user:
        raise_not_found("ユーザー")

    return APIResponse(
        message="ユーザー情報を取得しました",
        data=user
    )

@router.get("/me", response_model=APIResponse[UserSchema])
async def get_my_info(current_user = Depends(get_current_user)):
    return APIResponse(
        message="ユーザー情報を取得しました",
        data=current_user
    )


@router.post("/", response_model=APIResponse[UserSchema], status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserSchema, db_session: AsyncSession = Depends(get_db_session)
):
    created_user = await create_user(db_session, user)
    if not created_user:
        raise_bad_request("ユーザー作成に失敗しました")

    return APIResponse(
        message="ユーザーを作成しました",
        data=created_user
    )

@router.post("/login")
async def read_user_by_id_and_password_endpoint(
    user_id: str, password: str, db_session: AsyncSession = Depends(get_db_session)
):
    user = await get_user_by_id_and_password(db_session, user_id, password)
    if not user:
        raise_bad_request("認証失敗")

    token = create_access_token(user.user_id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user.model_dump()
    }

@router.put("/{user_id}", response_model=APIResponse[UserSchema])
async def update_user_endpoint(
    user_id: str, user: UserSchema, db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    updated_user = await update_user(db_session, user_id, user)
    if not updated_user:
        raise_not_found("ユーザー")

    return APIResponse(
        message="ユーザー情報を更新しました",
        data=updated_user
    )

@router.delete("/{user_id}", response_model=APIResponse[None])
async def delete_user_endpoint(
    user_id: str, db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    deleted = await delete_user(db_session, user_id)
    if not deleted:
        raise_not_found("ユーザー")

    return APIResponse(
        message="ユーザーを削除しました",
        data=None
    )
