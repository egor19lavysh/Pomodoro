from dataclasses import dataclass
from exception import TaskNotFoundException
from repository import TaskRepository, CacheTask
from schema import TaskCreateSchema, Task


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self) -> list[Task]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def get_task(self, task_id: int) -> Task | None:
        task = self.task_repository.get_task(task_id=task_id)
        if not task:
            raise TaskNotFoundException
        return Task.model_validate(task)

    def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = self.task_repository.create_task(task=body, user_id=user_id)
        task = self.task_repository.get_task(task_id=task_id)
        return Task.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int):
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        task = self.task_repository.update_name(task_id=task_id, name=name)
        return Task.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        self.task_repository.delete_task(task_id=task_id)

