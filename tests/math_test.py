import math
from itertools import permutations, product

import pytest

from atcoder.math import crt, floor_sum, inv_mod, pow_mod

from .utils.limits import numeric_limits


def floor_sum_naive(n: int, m: int, a: int, b: int) -> int:
    sum_ = 0
    for i in range(n):
        z = a * i + b
        sum_ += (z - z % m) // m
    return sum_


def is_prime_naive(n: int) -> bool:
    assert 0 <= n <= numeric_limits("int").max()
    if n == 0 or n == 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def test_PowMod() -> None:
    for a, b, c in product(range(-100, 101), range(101), range(1, 101)):
        assert pow(a, b, c) == pow_mod(a, b, c)


def test_InvBoundHand() -> None:
    assert inv_mod(-1, numeric_limits("ll").max()) == inv_mod(numeric_limits("ll").min(), numeric_limits("ll").max())
    assert 1 == inv_mod(numeric_limits("ll").max(), numeric_limits("ll").max() - 1)
    assert numeric_limits("ll").max() - 1 == inv_mod(numeric_limits("ll").max() - 1, numeric_limits("ll").max())
    assert 2 == inv_mod(numeric_limits("ll").max() // 2 + 1, numeric_limits("ll").max())


def test_InvMod() -> None:
    for a, b in product(range(-100, 101), range(1, 1000)):
        if math.gcd(a % b, b) != 1:
            continue
        c = inv_mod(a, b)
        assert 0 <= c
        assert c < b
        assert 1 % b == ((a * c) % b + b) % b


def test_InvModZero() -> None:
    assert 0 == inv_mod(0, 1)
    for i in range(10):
        assert 0 == inv_mod(i, 1)
        assert 0 == inv_mod(-i, 1)
        assert 0 == inv_mod(numeric_limits("ll").min() + i, 1)
        assert 0 == inv_mod(numeric_limits("ll").max() - i, 1)


def test_FloorSum() -> None:
    for n, m, a, b in product(
        range(20),
        range(1, 20),
        range(-20, 20),
        range(-20, 20),
    ):
        assert floor_sum_naive(n, m, a, b) == floor_sum(n, m, a, b)


def test_CRTHand() -> None:
    assert (5, 6) == crt([1, 2, 1], [2, 3, 2])


def test_CRT2() -> None:
    for a, b, c, d in product(
        range(1, 21),
        range(1, 21),
        range(-10, 11),
        range(-10, 11),
    ):
        res = crt([c, d], [a, b])
        if res[1] == 0:
            x = 0
            while x < a * b // math.gcd(a, b):
                assert x % a != c or x % b != d
                x += 1
            continue

        assert a * b // math.gcd(a, b), res[1]
        assert c % a == res[0] % a
        assert d % b == res[0] % b


def test_CRT3() -> None:
    for a, b, c, d, e, f in product(
        range(1, 6),
        range(1, 6),
        range(1, 6),
        range(-5, 6),
        range(-5, 6),
        range(-5, 6),
    ):
        res = crt([d, e, f], [a, b, c])
        lcm = math.lcm(a, b, c)
        if res[1] == 0:
            for x in range(lcm):
                assert x % a != d or x % b != e or x % c != f
            continue
        assert lcm == res[1]
        assert d % a == res[0] % a
        assert e % b == res[0] % b
        assert f % c == res[0] % c


def test_CRTOverflow() -> None:
    r0 = 0
    r1 = 1_000_000_000_000 - 2
    m0 = 900577
    m1 = 1_000_000_000_000
    res = crt([r0, r1], [m0, m1])
    assert m0 * m1 == res[1]
    assert r0 == res[0] % m0
    assert r1 == res[0] % m1


INF: int = numeric_limits("ll").max()

pred = []
for i in range(1, 11):
    pred.append(i)
    pred.append(INF - (i - 1))
pred.append(998244353)
pred.append(1_000_000_007)
pred.append(1_000_000_009)


class TestCRTBound:
    @pytest.mark.parametrize(
        ("a", "b"),
        [
            (INF, INF),
            (1, INF),
            (INF, 1),
            (7, INF),
            (INF // 337, 337),
            (2, (INF - 1) // 2),
        ],
    )
    def test_CRTBound1(self, a: int, b: int) -> None:
        for _ in range(2):
            for ans in pred:
                res = crt([ans % a, ans % b], [a, b])
                lcm = math.lcm(a, b)
                assert lcm == res[1]
                assert ans % lcm == res[0]
            a, b = b, a

    def test_CRTBound2(self) -> None:
        for factor_inf in permutations([49, 73, 127, 337, 92737, 649657]):
            for ans in pred:
                r = [ans % f for f in factor_inf]
                m = list(factor_inf)
                res = crt(r, m)
                assert ans % INF == res[0]
                assert INF == res[1]

    def test_CRTBound3(self) -> None:
        for factor_infn1 in permutations([2, 3, 715827883, 2147483647]):
            for ans in pred:
                r = [ans % f for f in factor_infn1]
                m = list(factor_infn1)
                res = crt(r, m)
                assert ans % (INF - 1) == res[0]
                assert INF - 1 == res[1]
