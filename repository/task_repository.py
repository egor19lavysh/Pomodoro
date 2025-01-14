from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from models import Tasks, Categories
from schema.task import Task


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> Tasks:
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            task: Tasks = session.execute(query).scalar_one_or_none()
        return task

    def get_tasks(self) -> list[Tasks] | None:
        query = select(Tasks)
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query).scalars()
            return tasks

    def create_task(self, task: Task) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def update_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)

    def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks] | None:
        query = select(Tasks).join(Categories, Tasks.id == Categories.id).where(category_name == Categories.name)
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query).scalars().all()
            return tasks
