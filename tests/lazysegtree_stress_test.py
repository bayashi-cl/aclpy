from dataclasses import dataclass
from functools import partial
from random import randint
from typing import Callable, cast

from atcoder.lazysegtree import lazysegtree

from .utils.random_ import randpair


class time_manager:
    def __init__(self, n: int) -> None:
        self.v = [-1] * n

    def action(self, l: int, r: int, time: int) -> None:
        for i in range(l, r):
            self.v[i] = time

    def prod(self, l: int, r: int) -> int:
        res = max(self.v[l:r], default=-1)
        return res


@dataclass
class S:
    l: int
    r: int
    time: int


@dataclass
class T:
    new_time: int


def op_ss(l: S, r: S) -> S:
    if l.l == -1:
        return r
    if r.l == -1:
        return l
    assert l.r == r.l
    return S(l.l, r.r, max(l.time, r.time))


def op_ts(l: T, r: S) -> S:
    if l.new_time == -1:
        return r
    assert r.time < l.new_time
    return S(r.l, r.r, l.new_time)


def op_tt(l: T, r: T) -> T:
    if l.new_time == -1:
        return r
    if r.new_time == -1:
        return l
    assert l.new_time > r.new_time
    return l


def e_s() -> S:
    return S(-1, -1, -1)


def e_t() -> T:
    return T(-1)


seg = cast(
    Callable[..., lazysegtree[S, T]],
    partial(lazysegtree, op_ss, e_s, op_ts, op_tt, e_t),
)


def test_NaiveTest() -> None:
    for n in range(1, 31):
        for ph in range(10):
            seg0 = seg(n)
            tm = time_manager(n)
            for i in range(n):
                seg0.set(i, S(i, i + 1, -1))
            now = 0
            for q in range(3000):
                ty = randint(0, 3)
                l, r = randpair(0, n)
                if ty == 0:
                    res = seg0.prod(l, r)
                    assert l == res.l
                    assert r == res.r
                    assert tm.prod(l, r) == res.time
                elif ty == 1:
                    res = seg0.get(l)
                    assert l == res.l
                    assert l + 1 == res.r
                    assert tm.prod(l, l + 1) == res.time
                elif ty == 2:
                    now += 1
                    seg0.apply(l, r, T(now))
                    tm.action(l, r, now)
                elif ty == 3:
                    now += 1
                    seg0.apply(l, T(now))
                    tm.action(l, l + 1, now)
                else:
                    assert False


def test_MaxRightTest():
    for n in range(1, 31):
        for ph in range(10):
            seg0 = seg(n)
            tm = time_manager(n)
            for i in range(n):
                seg0.set(i, S(i, i + 1, -1))
            now = 0
            for q in range(1000):
                ty = randint(0, 2)
                l, r = randpair(0, n)
                if ty == 0:

                    def g(s: S) -> bool:
                        if s.l == -1:
                            return True
                        assert s.l == l
                        assert s.time == tm.prod(l, s.r)
                        return s.r <= r

                    assert r == seg0.max_right(l, g)
                else:
                    now += 1
                    seg0.apply(l, r, T(now))
                    tm.action(l, r, now)


def test_MinLeftTest() -> None:
    for n in range(1, 30):
        for ph in range(10):
            seg0 = seg(n)
            tm = time_manager(n)
            for i in range(n):
                seg0.set(i, S(i, i + 1, -1))
            now = 0
            for q in range(1000):
                ty = randint(0, 2)
                l, r = randpair(0, n)
                if ty == 0:

                    def g(s: S) -> bool:
                        if s.l == -1:
                            return True
                        assert s.r == r
                        assert s.time == tm.prod(s.l, r)
                        return l <= s.l

                    assert l == seg0.min_left(r, g)
                else:
                    now += 1
                    seg0.apply(l, r, T(now))
                    tm.action(l, r, now)
