from clients import GoogleClient
from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, CacheTask, UserRepository
from database.accessor import get_db_session
from cache.accessor import get_redis_connection
from services import TaskService, UserService, AuthService
from fastapi import Depends, Request, security, Security, HTTPException

from settings import settings


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_repository() -> CacheTask:
    redis = get_redis_connection()
    return CacheTask(redis)


def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session=db_session)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: CacheTask = Depends(get_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository,
        task_cache
    )


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=settings, google_client=google_client)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id
