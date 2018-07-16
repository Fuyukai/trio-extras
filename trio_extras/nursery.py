import trio
from async_generator import asynccontextmanager
from functools import partial
from typing import Callable, Any, Awaitable, List, AsyncContextManager

from trio_extras.promise import Promise


class ReturningNursery(object):
    """
    Represents a "returning" nursery - a nursery that lets you await for the result from a
    spawned task.
    """
    def __init__(self, real_nursery):
        """
        :param real_nursery: The :class:`trio.Nursery` that is the real nursery for this
            returning nursery.
        """
        self._real_nursery = real_nursery

    def start_soon(self, fn: Callable[..., Awaitable[Any]], *args: Any) -> Promise:
        """
        Starts the specified task soon, returning a :class:`.Promise` that can be used to
        get the result of the task.

        Usage::

            async with trio_extras.open_returning_nursery() as n:
                n.start_soon(task_you_dont_care_about)
                task = n.start_soon(task_you_do_care_about)
                result = await task.wait_for_result()

        :param fn: The async function to start as an async task.
        :return: A :class:`.TaskAwaitable` that can be waited on to get the result of the task.
        """
        p = partial(fn, *args)
        status = Promise()
        self._real_nursery.start_soon(self._wait_wrapper, p, status)
        return status

    async def _wait_wrapper(self, cbl, status: Promise):
        """
        Wraps an async function, providing a return value.
        """
        result = await cbl()
        status.set(result)


@asynccontextmanager
async def open_returning_nursery() -> AsyncContextManager[ReturningNursery]:
    """
    Opens a **returning nursery** - a nursery that returns task wrappers that are awaitable.
    """
    # we have to open a real nursery, first
    async with trio.open_nursery() as n:
        our_nursery = ReturningNursery(n)
        yield our_nursery


async def collect(*cbls: Callable[..., Awaitable[Any]]) -> List[Any]:
    """
    Collects a list of async functions, returning a list of results.

    :param cbls: The async functions to call. Use a :class:`functools.Partial` to pass arguments.
    :return: A list of results.
    """
    async with open_returning_nursery() as n:
        tasks = [n.start_soon(cbl) for cbl in cbls]

    return [await result.wait() for result in tasks]
