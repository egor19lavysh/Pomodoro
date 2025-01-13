from dataclasses import dataclass

from repository import TaskRepository, CacheTask
from schema.task import Task


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
