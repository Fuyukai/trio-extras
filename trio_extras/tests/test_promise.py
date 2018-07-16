"""
Tests Promises.
"""
import trio

from trio_extras.promise import Promise


async def test_promise_set():
    p = Promise()

    async def first():
        p.set("abc")

    async def second():
        result = await p.wait()
        assert result == "abc"
        p.set("def")

    async with trio.open_nursery() as n:
        n.start_soon(second)
        n.start_soon(first)

    assert await p.wait() == "def"


async def test_promise_reset():
    p = Promise()
    p.set("heck")
    p.clear()
    assert not p.is_set()

