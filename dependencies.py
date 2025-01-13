from repository import TaskRepository, CacheTask
from database.database import get_db_session
from cache.accessor import get_redis_connection
from services import TaskService
from fastapi import Depends


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_repository() -> CacheTask:
    redis = get_redis_connection()
    return CacheTask(redis)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: CacheTask = Depends(get_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository,
        task_cache
    )
