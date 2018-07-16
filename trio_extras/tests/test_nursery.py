"""
Tests the returning nursery.
"""
from functools import partial

from trio_extras.nursery import open_returning_nursery, collect


async def test_nursery_works():
    async def first(a, b):
        return a + b

    async def second():
        return "basculin"

    async with open_returning_nursery() as n:
        t1 = n.start_soon(first, 1, 2)
        t2 = n.start_soon(second)

        assert (await t1.wait()) == 3

    assert (await t2.wait()) == "basculin"


async def test_collect():
    async def add(a, b):
        return a + b

    results = await collect(partial(add, 1, 2), partial(add, 3, 4), partial(add, 5, 6))
    assert results == [3, 7, 11]