from repository import TaskRepository, CacheTask, UserRepository
from database.accessor import get_db_session
from cache.accessor import get_redis_connection
from services import TaskService, UserService, AuthService
from fastapi import Depends


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


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository)
