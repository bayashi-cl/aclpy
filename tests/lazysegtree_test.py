from functools import partial
from typing import Callable, cast

import pytest

from atcoder.lazysegtree import lazysegtree

from .utils.marker import skip_cppassert


class starry:
    @staticmethod
    def op_ss(a: int, b: int) -> int:
        return max(a, b)

    @staticmethod
    def op_ts(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def op_tt(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def e_s() -> int:
        return -1_000_000_000

    @staticmethod
    def e_t() -> int:
        return 0


starry_seg = cast(
    Callable[..., lazysegtree[int, int]],
    partial(
        lazysegtree,
        starry.op_ss,
        starry.e_s,
        starry.op_ts,
        starry.op_tt,
        starry.e_t,
    ),
)


class TestZero:
    def test_Zero1(self) -> None:
        s = starry_seg(0)
        assert -1_000_000_000 == s.all_prod()

    def test_Zero2(self) -> None:
        s = starry_seg()
        assert -1_000_000_000 == s.all_prod()

    def test_Zero3(self) -> None:
        s = starry_seg(10)
        assert -1_000_000_000 == s.all_prod()


def test_Assign() -> None:
    seg0 = starry_seg()
    seg0 = starry_seg(10)  # noqa:F841


class TestInvalid:
    def test_Invalid1(self) -> None:
        with pytest.raises(ValueError):
            s = starry_seg(-1)  # noqa:F841

    @skip_cppassert
    def test_Invalid2(self):
        s = starry_seg(10)

        with pytest.raises(AssertionError):
            s.get(-1)
            s.get(10)

            s.prod(-1, -1)
            s.prod(3, 2)
            s.prod(0, 11)
            s.prod(-1, 11)


def test_NaiveProd() -> None:
    for n in range(51):
        seg = starry_seg(n)
        p = [(i * i + 100) % 31 for i in range(n)]
        for i in range(n):
            seg.set(i, p[i])
        for l in range(n + 1):
            for r in range(l, n + 1):
                e = max(p[l:r], default=-1_000_000_000)
                assert e == seg.prod(l, r)


def test_Usage() -> None:
    seg = starry_seg([0] * 10)
    assert 0 == seg.all_prod()
    seg.apply(0, 3, 5)
    assert 5 == seg.all_prod()
    seg.apply(2, -10)
    assert -5 == seg.prod(2, 3)
    assert 0 == seg.prod(2, 4)
