from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User as UserModel  # SQLAlchemyのORMモデル
from schemas.user import User as UserSchema  # PydanticのAPIスキーマ

async def get_user_by_id_and_password(session: AsyncSession, user_id: str, password: str) -> UserSchema | None:
    """
    ユーザーIDとパスワードでユーザーを取得する関数（ログイン認証用）
    
    Args:
        session (AsyncSession): 非同期データベースセッション
            - SQLAlchemyの非同期セッションオブジェクト
            - データベースとの接続を管理
        user_id (str): 検索対象のユーザーID
        password (str): 照合するパスワード（平文）
            ※実際のアプリではハッシュ化されたパスワードと比較すべき

    Returns:
        UserSchema | None: 
            - 認証成功時: ユーザー情報のPydanticモデル
            - 認証失敗時: None
    
    Raises:
        Exception: データベースアクセス時のエラー
    
    使用例:
        user = await get_user_by_id_and_password(session, "user123", "password")
        if user:
            print("ログイン成功")
        else:
            print("ログイン失敗")
    """

    try:
        # SQL SELECT文を構築してユーザーを検索
        # WHERE句で user_id AND password の両方が一致するレコードを検索
        result = await session.execute(
            select(UserModel).where(UserModel.user_id == user_id, UserModel.password == password)
        )
        # scalar_one_or_none(): 結果が1件の場合はそのオブジェクト、0件の場合はNoneを返す
        user = result.scalar_one_or_none()
        # SQLAlchemyモデルをPydanticスキーマに変換
        return UserSchema.model_validate(user) if user else None
    except Exception as e:
        # データベースエラーをキャッチして安全に処理
        print(f"Error occurred while fetching user: {e}")
        return None

async def get_user_by_id(session:AsyncSession, user_id: str) -> UserSchema | None:
    """
    ユーザーIDでユーザー情報を取得する関数
    
    Args:
        session (AsyncSession): 非同期データベースセッション
        user_id (str): 検索対象のユーザーID
    
    Returns:
        UserSchema | None:
            - 見つかった場合: ユーザー情報のPydanticモデル
            - 見つからない場合: None
    
    Note:
        この関数はパスワード認証なしでユーザー情報を取得します。
        プロフィール表示や管理者機能などで使用されます。
    """
    try:
        # ユーザーIDのみでユーザーを検索（パスワード認証なし）
        result = await session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        # SQLAlchemyモデルをPydanticスキーマに変換
        return UserSchema.model_validate(user) if user else None
    except Exception as e:
        # データベースエラーの安全な処理
        print(f"Error occurred while fetching user: {e}")
        return None
    
async def get_users(session: AsyncSession) -> list[UserSchema] | None:
    """
    ユーザーを取得する関数（ログイン認証用）
    
    Args:
        session (AsyncSession): 非同期データベースセッション
            - SQLAlchemyの非同期セッションオブジェクト
            - データベースとの接続を管理
        user_id (str): 検索対象のユーザーID
        password (str): 照合するパスワード（平文）
            ※実際のアプリではハッシュ化されたパスワードと比較すべき

    Returns:
        UserSchema | None: 
            - 認証成功時: ユーザー情報のPydanticモデル
            - 認証失敗時: None
    
    Raises:
        Exception: データベースアクセス時のエラー
    
    使用例:
        user = await get_user_by_id_and_password(session, "user123", "password")
        if user:
            print("ログイン成功")
        else:
            print("ログイン失敗")
    """

    try:
        # SQL SELECT文を構築してユーザーを検索
        # WHERE句で user_id AND password の両方が一致するレコードを検索
        result = await session.execute(select(UserModel))
        users = result.scalars().all()
        # scalar_one_or_none(): 結果が1件の場合はそのオブジェクト、0件の場合はNoneを返す
        return [UserSchema.model_validate(user) for user in users]
    except Exception as e:
        # データベースエラーをキャッチして安全に処理
        print(f"Error occurred while fetching user: {e}")
        return None
    
async def create_user(session: AsyncSession, user_data: UserSchema) -> UserSchema | None:
    """
    新しいユーザーをデータベースに登録する関数
    
    Args:
        session (AsyncSession): 非同期データベースセッション
        user_data (UserSchema): 作成するユーザーのデータ（Pydanticモデル）
    
    Returns:
        UserSchema: 作成されたユーザーのモデル（DBから取得した最新データ）
        None: 作成に失敗した場合
    
    処理の流れ:
        1. PydanticモデルをSQLAlchemyモデルに変換
        2. セッションに追加
        3. データベースにコミット（永続化）
        4. 最新データでオブジェクトを更新
    
    Note:
        - model_dump(): PydanticモデルをPython辞書に変換
        - session.add(): セッションにオブジェクトを追加（まだDBには保存されない）
        - session.commit(): 変更をデータベースに永続化
        - session.refresh(): DBから最新データを取得してオブジェクトを更新
    """
    try:
        # Pydanticモデルの辞書データを使ってSQLAlchemyモデルのインスタンスを作成
        new_user = UserModel(**user_data.model_dump())
        
        # セッションにオブジェクトを追加（まだDBには保存されない）
        session.add(new_user)
        
        # データベースに変更をコミット（実際にDBに保存）
        await session.commit()
        
        # DBから最新のデータを取得してオブジェクトを更新
        # これにより、auto_incrementのIDなどが反映される
        await session.refresh(new_user)
        
        # SQLAlchemyモデルをPydanticスキーマに変換
        return UserSchema.model_validate(new_user)
    except Exception as e:
        # エラー時にロールバックを実行
        await session.rollback()
        print(f"Error occurred while creating user: {e}")
        return None

async def update_user(
        session: AsyncSession,
        user_id: str,
        user_data: UserSchema) -> UserSchema | None:
    """
    既存ユーザーの情報を更新する関数
    
    Args:
        session (AsyncSession): 非同期データベースセッション
        user_id (str): 更新対象のユーザーID
        user_data (UserSchema): 更新するデータ（Pydanticモデル）
    
    Returns:
        UserSchema | None:
            - 更新成功時: 更新後のユーザー情報
            - 更新失敗時: None（ユーザーが見つからない、またはエラー）
    
    処理の流れ:
        1. 更新対象のユーザーをIDで検索
        2. ユーザーが存在する場合、各属性を更新
        3. 変更をデータベースにコミット
        4. 最新データでオブジェクトを更新
    
    Note:
        - setattr(): オブジェクトの属性を動的に設定
        - この方法により、Pydanticモデルの全フィールドを一括更新
    """
    try:
        # 既存のユーザーを検索
        result = await session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # ユーザーが見つかった場合、各フィールドを更新
            # model_dump()でPydanticモデルを辞書に変換し、各項目を設定
            for key, value in user_data.model_dump().items():
                # setattr(オブジェクト, 属性名, 値)で動的に属性を設定
                setattr(user, key, value)
            
            # 変更をデータベースに保存
            await session.commit()
            
            # DBから最新データを取得して反映
            await session.refresh(user)
            
            # SQLAlchemyモデルをPydanticスキーマに変換
            return UserSchema.model_validate(user)
        
        # ユーザーが見つからない場合
        return None
        
    except Exception as e:
        # エラー時にロールバックを実行
        await session.rollback()
        print(f"Error occurred while updating user: {e}")
        return None

async def delete_user(session: AsyncSession, user_id: str) -> bool:
    """
    ユーザーをデータベースから削除する関数
    
    Args:
        session (AsyncSession): 非同期データベースセッション
        user_id (str): 削除対象のユーザーID
    
    Returns:
        bool:
            - True: 削除成功
            - False: 削除失敗（ユーザーが見つからない、またはエラー）
    
    処理の流れ:
        1. 削除対象のユーザーをIDで検索
        2. ユーザーが存在する場合、セッションから削除
        3. 変更をデータベースにコミット
    
    Note:
        - 外部キー制約によって関連するアイテム（TODO）も削除される可能性があります
        - CASCADE設定により、このユーザーに紐づくTODOアイテムも自動削除されます
    
    Warning:
        この操作は取り消せません。重要なデータの削除前には
        必ず確認処理を実装することを推奨します。
    """
    try:
        # 削除対象のユーザーを検索
        result = await session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # ユーザーが見つかった場合、セッションから削除
            await session.delete(user)
            
            # 変更をデータベースに保存（実際に削除実行）
            await session.commit()
            
            return True  # 削除成功
        
        # ユーザーが見つからない場合
        return False
        
    except Exception as e:
        # エラー時にロールバックを実行
        await session.rollback()
        print(f"Error occurred while deleting user: {e}")
        return False