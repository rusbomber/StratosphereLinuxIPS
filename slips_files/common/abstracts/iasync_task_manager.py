import asyncio
import traceback
from asyncio import Task


class AsyncTaskManager:
    """
    boilerplate for async classes that are not modules and need to handle
    task creation and gathering
    """

    def __init__(self) -> None:
        self._tasks: list[asyncio.Task] = []

    def _handle_task_exception(self, task: asyncio.Task) -> None:
        try:
            exc = task.exception()
        except asyncio.CancelledError:
            return
        if exc:
            print(f"Unhandled exception in task: {exc}")
            traceback.print_exception(type(exc), exc, exc.__traceback__)

    def create_task(self, func, *args, **kwargs) -> Task:
        """
        wrapper for asyncio.create_task
        The goal here is to add a callback to tasks to be able to handle
        exceptions. because asyncio Tasks do not raise exceptions
        """
        task = asyncio.create_task(func(*args, **kwargs))
        task.add_done_callback(self._handle_task_exception)
        self._tasks.append(task)
        return task

    async def shutdown_gracefully(self) -> None:
        if not self._tasks:
            return
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
