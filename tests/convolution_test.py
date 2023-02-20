from functools import partial
from random import randint
from typing import Type, overload

import pytest

from atcoder.convolution import (
    convolution,
    convolution_998244353,
    convolution_1000000007,
    convolution_ll,
)
from atcoder.modint import modint998244353, modint1000000007

from .utils.limits import numeric_limits


def conv_ll_naive(a: list[int], b: list[int]) -> list[int]:
    n = len(a)
    m = len(b)
    c = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            c[i + j] += a[i] * b[j]
    return c


@overload
def conv_naive(a: list[modint998244353], b: list[modint998244353]) -> list[modint998244353]:
    ...


@overload
def conv_naive(a: list[modint1000000007], b: list[modint1000000007]) -> list[modint1000000007]:
    ...


def conv_naive(a, b):
    mint = a[0].__class__
    n = len(a)
    m = len(b)
    c = [mint(0) for _ in range(n + m - 1)]
    for i in range(n):
        for j in range(m):
            c[i + j] += a[i] * b[j]
    return c


def conv_mod_naive(MOD: int, a: list[int], b: list[int]):
    n = len(a)
    m = len(b)
    c = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            c[i + j] += a[i] * b[j] % MOD
            if c[i + j] >= MOD:
                c[i + j] -= MOD
    return c


def test_Empty() -> None:
    assert [] == convolution_998244353([], [])
    assert [] == convolution_998244353([], [1, 2])
    assert [] == convolution_998244353([1, 2], [])
    assert [] == convolution_998244353([1], [])

    assert [] == convolution([], [])
    assert [] == convolution([], [modint998244353(1), modint998244353(2)])


def test_Mid() -> None:
    mt = partial(randint, 0, numeric_limits("uint").max())
    n = 1234
    m = 2345
    a = [modint998244353(mt()) for _ in range(n)]
    b = [modint998244353(mt()) for _ in range(m)]
    assert conv_naive(a, b) == convolution(a, b)


@pytest.mark.parametrize(("s_mint",), [(modint998244353,), (modint1000000007,)])
def test_SimpleMod(s_mint: Type):
    # only support 1000000007 and 998244353.
    mt = partial(randint, 0, numeric_limits("uint").max())
    for n in range(1, 20):
        for m in range(1, 20):
            a = [s_mint(mt()) for _ in range(n)]
            b = [s_mint(mt()) for _ in range(m)]
            assert conv_naive(a, b) == convolution(a, b)


@pytest.mark.skip(reason="support only long long.")
class TestSimpleInt:
    def test_SimpleInt(self) -> None:
        ...


@pytest.mark.skip(reason="support only long long.")
class TestSimpleUint:
    def test_SimpleUInt(self) -> None:
        ...


class TestSimpleLL:
    def test_SimpleLL1(self):
        MOD = 998244353
        mt = partial(randint, 0, numeric_limits("uint").max())
        for n in range(1, 20):
            for m in range(1, 20):
                a = [mt() for _ in range(n)]
                b = [mt() for _ in range(m)]
                assert conv_mod_naive(MOD, a, b) == convolution_998244353(a, b)

    def test_SimpleLL2(self):
        MOD = 1000000007
        mt = partial(randint, 0, numeric_limits("uint").max())
        for n in range(1, 20):
            for m in range(1, 20):
                a = [mt() for _ in range(n)]
                b = [mt() for _ in range(m)]
                assert conv_mod_naive(MOD, a, b) == convolution_1000000007(a, b)


@pytest.mark.skip(reason="support only long long.")
class TestSimpleULL:
    def test_SimpleULL(self) -> None:
        ...


@pytest.mark.skip(reason="support only long long.")
class TestSimpleInt128:
    def test_SimpleInt128(self) -> None:
        ...


@pytest.mark.skip(reason="support only long long.")
class TestSimpleUInt128:
    def test_SimpleUInt128(self) -> None:
        ...


def test_ConvLL() -> None:
    mt = partial(randint, 0, numeric_limits("uint").max())
    for n in range(1, 20):
        for m in range(1, 20):
            a = [(mt() % 1_000_000) - 500_000 for _ in range(n)]
            b = [(mt() % 1_000_000) - 500_000 for _ in range(m)]
            assert conv_ll_naive(a, b) == convolution_ll(a, b)


def test_ConvLLBound() -> None:
    MOD1 = 469762049  # 2^26
    MOD2 = 16777216  # 2^25
    MOD3 = 754974721  # 2^24
    M2M3 = MOD2 * MOD3
    M1M3 = MOD1 * MOD3
    M1M2 = MOD1 * MOD2
    for i in range(-1000, 1001):
        a = [0 - M1M2 - M1M3 - M2M3 + i]
        b = [1]

        assert a == convolution_ll(a, b)

    for i in range(1000):
        a = [numeric_limits("ll").min() + i]
        b = [1]
        assert a == convolution_ll(a, b)

    for i in range(1000):
        a = [numeric_limits("ll").max() - i]
        b = [1]
        assert a == convolution_ll(a, b)


@pytest.mark.skip(reason="only support 1000000007 and 998244353.")
class TestConv:
    def test_Conv641(self) -> None:
        ...

    def test_Conv18433(self) -> None:
        ...

    def test_Conv2(self) -> None:
        ...

    def test_Conv257(self) -> None:
        ...

    def test_Conv2147483647(self) -> None:
        ...

    def test_Conv2130706433(self) -> None:
        ...
