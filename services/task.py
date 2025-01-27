from dataclasses import dataclass
from exception import TaskNotFoundException
from repository import TaskRepository, CacheTask
from schema import TaskCreateSchema, Task


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    async def get_tasks(self) -> list[Task]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def get_task(self, task_id: int) -> Task | None:
        task = self.task_repository.get_task(task_id=task_id)
        if not task:
            raise TaskNotFoundException
        return await Task.model_validate(task)

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = await self.task_repository.create_task(task=body, user_id=user_id)
        task = await self.task_repository.get_task(task_id=task_id)
        return await Task.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int):
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        task = await self.task_repository.update_name(task_id=task_id, name=name)
        return await Task.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        await self.task_repository.delete_task(task_id=task_id)

