from fastapi import APIRouter, status, Depends
from schema.task import Task
from repository import TaskRepository, CacheTask
from typing import Annotated
from dependencies import get_tasks_repository, get_task_service
from services.task import TaskService
router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[Task] | None)
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    return task_service.get_tasks()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task = task_repository.get_task(task_id)
    return task


@router.post("/", response_model=Task)
async def create_task(task: Task, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.patch("/{task_id}")
async def patch_task(task_id: int,
                     name: str,
                     task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    return task_repository.update_name(task_id, name)


@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_repository.delete_task(task_id)
    return status.HTTP_204_NO_CONTENT
