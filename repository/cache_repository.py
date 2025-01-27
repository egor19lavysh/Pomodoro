import json

from redis import asyncio as Redis

from schema.task import Task


class CacheTask:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[Task]:
        async with self.redis as redis:
            tasks_json = await redis.lrange("tasks", 0, -1)
            return [Task.model_validate(json.loads(task)) for task in tasks_json]

    async def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.json() for task in tasks]
        async with self.redis as redis:
            await self.redis.lpush("tasks", *tasks_json)
