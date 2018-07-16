"""
Represents a promise - an awaitable event that can hold some data, too.
"""
import trio
from typing import Any


class Promise(object):
    """
    A very simple wrapper over an event that allows providing some data alongside the event.

    Usage::

        p = Promise()

        # task A
        action = await some_long_task()
        p.set(action)

        # task B
        result = await p.wait()
    """

    def __init__(self):
        self._event = trio.Event()
        self._value = None

    async def wait(self) -> Any:
        """
        Waits for this promise to have some data.
        """
        await self._event.wait()
        return self._value

    def set(self, data: Any):
        """
        Sets the result of this promise.
        """
        self._value = data
        self._event.set()

    def is_set(self) -> bool:
        """
        Returns if this Promise is set or not.
        """
        return self._event.is_set()

    def clear(self):
        """
        Resets this promise.
        """
        self._value = None
        self._event.clear()

    def statistics(self):
        """
        Returns the statistics for this promise, copied from the underlying event.
        """
        return self._event.statistics()
