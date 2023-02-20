from functools import partial
from typing import Callable, Generic, TypeVar, cast

import pytest

from atcoder.segtree import segtree

from .utils.marker import skip_cppassert

S = TypeVar("S")


class segtree_naive(Generic[S]):
    def __init__(self, op: Callable[[S, S], S], e: Callable[[], S], n: int) -> None:
        self.n = n
        self.op = op
        self.e = e
        self.d = [self.e() for _ in range(self.n)]

    def set(self, p: int, x: S) -> None:
        self.d[p] = x

    def get(self, p: int) -> S:
        return self.d[p]

    def prod(self, l: int, r: int) -> S:
        sum_ = self.e()
        for i in range(l, r):
            sum_ = self.op(sum_, self.d[i])
        return sum_

    def all_prod(self) -> S:
        return self.prod(0, self.n)

    def max_right(self, l: int, f: Callable[[S], bool]) -> int:
        sum_ = self.e()
        assert f(sum_)
        for i in range(l, self.n):
            sum_ = self.op(sum_, self.d[i])
            if not f(sum_):
                return i
        return self.n

    def min_left(self, r: int, f: Callable[[S], bool]) -> int:
        sum_ = self.e()
        assert f(sum_)
        for i in reversed(range(r)):
            sum_ = self.op(self.d[i], sum_)
            if not f(sum_):
                return i + 1
        return 0


def op(a: str, b: str) -> str:
    assert a == "$" or b == "$" or a <= b
    if a == "$":
        return b
    if b == "$":
        return a
    return a + b


def e() -> str:
    return "$"


seg = cast(Callable[..., segtree[str]], partial(segtree, op, e))
seg_naive = cast(Callable[..., segtree_naive[str]], partial(segtree_naive, op, e))


class TestZero:
    def test_Zero1(self) -> None:
        s = seg(0)
        assert "$" == s.all_prod()

    def test_Zero2(self) -> None:
        s = seg()
        assert "$" == s.all_prod()


class TestInvalid:
    def test_Invalid1(self) -> None:
        with pytest.raises(ValueError):
            s = seg(-1)  # noqa:F841

    @skip_cppassert
    def test_Invalid2(self) -> None:
        s = seg(10)
        with pytest.raises(AssertionError):
            s.get(-1)
            s.get(10)

            s.prod(-1, -1)
            s.prod(3, 2)
            s.prod(0, 11)
            s.prod(-1, 11)

            s.max_right(11, lambda s: True)
            s.max_right(-1, lambda s: True)
            s.max_right(0, lambda s: False)


def test_One() -> None:
    s: segtree[str] = seg(1)
    assert "$" == s.all_prod()
    assert "$" == s.get(0)
    assert "$" == s.prod(0, 1)
    s.set(0, "dummy")
    assert "dummy" == s.get(0)
    assert "$" == s.prod(0, 0)
    assert "dummy" == s.prod(0, 1)
    assert "$" == s.prod(1, 1)


y = ""


def leq_y(x: str) -> bool:
    return len(x) <= len(y)


def test_CompareNaive() -> None:
    global y
    for n in range(30):
        seg0 = seg_naive(n)
        seg1 = seg(n)
        for i in range(n):
            s = chr(ord("a") + i)
            seg0.set(0, s)
            seg1.set(0, s)

        for l in range(n + 1):
            for r in range(l, n + 1):
                assert seg0.prod(l, r) == seg1.prod(l, r)

        for l in range(n + 1):
            for r in range(l, n + 1):
                y = seg1.prod(l, r)
                assert seg0.max_right(l, leq_y) == seg1.max_right(l, leq_y)
                assert seg0.max_right(l, leq_y) == seg1.max_right(l, lambda x: len(x) <= len(y))

        for r in range(n + 1):
            for l in range(r + 1):
                y = seg1.prod(l, r)
                assert seg0.min_left(r, leq_y) == seg1.min_left(r, leq_y)
                assert seg0.min_left(r, leq_y) == seg1.min_left(r, lambda x: len(x) <= len(y))


def test_Assign() -> None:
    seg0 = seg()
    seg0 = seg(10)  # noqa:F841
