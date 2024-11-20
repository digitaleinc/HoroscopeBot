import asyncio
from typing import List, Coroutine

from tgtarologistbot.src.core import logger


class TaskManager:
    _instance = None
    _coroutines: List[asyncio.Task] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_task(self, coro: Coroutine):
        """Добавляет асинхронную задачу в список и сразу запускает её."""
        task = asyncio.create_task(coro)
        self._coroutines.append(task)
        logger.info(f"Task started: {coro}")

    def get_tasks(self):
        """Возвращает список текущих задач."""
        return self._coroutines