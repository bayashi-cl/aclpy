from math import gcd

import pytest

from atcoder.modint import modint, modint0, modint998244353, modint1000000007

from .utils.limits import numeric_limits


def test_StaticMod() -> None:
    assert modint998244353.mod() == 998244353
    assert modint1000000007.mod() == 1000000007


def test_DynamicBorder() -> None:
    mint = modint
    mod_upper = numeric_limits("int").max()
    for mod in range(mod_upper, mod_upper - 1, -1):
        mint.set_mod(mod)
        v: list[int] = []
        for i in range(10):
            v.append(i)
            v.append(mod - i)
            v.append(mod // 2 + i)
            v.append(mod // 2 - i)

        for a in v:
            assert ((a * a) % mod * a) % mod == (mint(a).pow(3)).val()
            for b in v:
                assert (a + b) % mod == (mint(a) + mint(b)).val()
                assert (a - b) % mod == (mint(a) - mint(b)).val()
                assert (a * b) % mod == (mint(a) * mint(b)).val()


@pytest.mark.skip(reason="unsigned long long")
def test_ULL() -> None:
    pass


class TestMod1:
    def test_Mod1D(self) -> None:
        modint.set_mod(1)
        for i in range(100):
            for j in range(100):
                assert (modint(i) * modint(j)).val() == 0

        assert (modint(1234) + modint(5678)).val() == 0
        assert (modint(1234) - modint(5678)).val() == 0
        assert (modint(1234) * modint(5678)).val() == 0
        assert (modint(1234).pow(5678)).val() == 0
        assert 0 == modint(0).inv().val()
        assert 0 == modint(True).val()

    @pytest.mark.skip(reason="non-type template")
    def test_Mod1S(self) -> None:
        ...


INT32_MAX = numeric_limits("int").max()


class TestModIntMax:
    def test_ModIntMaxD(self) -> None:
        modint.set_mod(INT32_MAX)
        for i in range(0):
            for j in range(100):
                assert (modint(i) * modint(j)).val() == i * j
        assert (modint(1234) + modint(5678)).val() == 1234 + 5678
        assert (modint(1234) - modint(5678)).val() == INT32_MAX - 5678 + 1234
        assert (modint(1234) * modint(5678)).val() == 1234 * 5678

    @pytest.mark.skip(reason="non-type template")
    def test_ModIntMaxS(self) -> None:
        ...


@pytest.mark.skip(reason="__int128")
class TestInt128:
    def test_Int128D(self) -> None:
        ...

    def testInt128S(self) -> None:
        ...


class TestInv:
    @pytest.mark.skip(reason="non-type template")
    def test_InvS1(self) -> None:
        ...

    @pytest.mark.skip(reason="non-type template")
    def test_InvS2(self) -> None:
        ...

    def test_InvS3(self) -> None:
        for i in range(1, 100000):
            x = modint1000000007(i).inv().val()
            assert 1 == (x * i) % 1_000_000_007

    @pytest.mark.skip(reason="non-type template")
    def test_InvS4(self) -> None:
        ...

    def test_InvD1(self) -> None:
        modint.set_mod(998244353)
        for i in range(1, 100000):
            x = modint(i).inv().val()
            assert 0 <= x
            assert 998244353 - 1 >= x
            assert 1 == (x * i) % 998244353

    def test_InvD2(self) -> None:
        modint.set_mod(1_000_000_008)
        for i in range(1, 100000):
            if gcd(i, 1_000_000_008) != 1:
                continue
            x = modint(i).inv().val()
            assert 1 == (x * i) % 1_000_000_008

    def test_InvD3(self) -> None:
        modint.set_mod(INT32_MAX)
        for i in range(1, 100000):
            if gcd(i, INT32_MAX) != 1:
                continue
            x = modint(i).inv().val()
            assert 1 == (x * i) % INT32_MAX


class TestConstUsage:
    def test_ConstUsageS(self) -> None:
        # use 998244353 instead of 11
        sint = modint998244353
        a = sint(9)
        assert 9 == a.val()

    def test_ConstUsageD(self) -> None:
        dint = modint
        dint.set_mod(11)
        b = dint(9)
        assert 9 == b.val()


@pytest.mark.skip(reason="increment")
class TestIncrement:
    def test_IncrementS(self) -> None:
        ...

    def test_IncrementD(self) -> None:
        ...


def test_StaticUsage() -> None:
    # use 998244353 instead of 11
    mint = modint998244353
    assert 998244353 == mint.mod()
    # cannot `int == modint`
    assert 4 == (+mint(4)).val()
    assert 998244349 == (-mint(4)).val()

    assert not mint(1) == mint(3)
    assert mint(1) != mint(3)
    assert mint(1) == mint(998244354)
    assert not mint(1) != mint(998244354)

    # with pytest.raises(AssertionError):
    #     mint(3).pow(-1)


def test_DynamicUsage() -> None:
    assert 998244353 == modint0.mod()
    mint = modint
    mint.set_mod(998244353)
    assert 998244353 == mint.mod()
    assert 3 == (mint(1) + mint(2)).val()
    assert 3 == (1 + mint(2)).val()
    assert 3 == (mint(1) + 2).val()

    mint.set_mod(3)
    assert 3 == mint.mod()
    assert 1 == (mint(2) - mint(1)).val()
    assert 0 == (mint(1) + mint(2)).val()

    mint.set_mod(11)
    assert 11 == mint.mod()
    assert 4 == (mint(3) * mint(5)).val()

    assert 4 == (+mint(4)).val()
    assert 7 == (-mint(4)).val()

    assert not mint(1) == mint(3)
    assert mint(1) != mint(3)
    assert mint(1) == mint(12)
    assert not mint(1) != mint(12)

    # with pytest.raises(AssertionError):
    #     mint(3).pow(-1)


def test_Constructor() -> None:
    modint.set_mod(11)
    assert 1 == modint(True).val()
    assert 3 == modint(3).val()
    assert 1 == modint(-10).val()

    assert 2 == (1 + modint(1)).val()

    m = modint()
    0 == m.val()


def test_ConstructorStatic() -> None:
    mint = modint998244353
    assert 1 == mint(True).val()
    assert 3 == mint(3).val()
    assert 998244343 == mint(-10).val()

    assert 2 == (1 + mint(1)).val()

    m = mint()
    assert 0 == m.val()
