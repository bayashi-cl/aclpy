import pytest

from atcoder.fenwicktree import fenwick_tree
from atcoder.modint import modint, modint998244353

from .utils.limits import numeric_limits
from .utils.marker import skip_cppassert


class TestEmpty:
    def test_Empty1(self) -> None:
        fw_ll = fenwick_tree()
        assert 0 == fw_ll.sum(0, 0)

    @pytest.mark.skip(reason="TODO: support modint")
    def test_Empty2(self) -> None:
        fw_modint = ...
        assert 0 == fw_modint.sum(0, 0).val()


def test_Assign() -> None:
    fw = fenwick_tree()
    fw = fenwick_tree(10)  # noqa:F841


class TestZero:
    def test_Zero1(self) -> None:
        fw_ll = fenwick_tree(0)
        assert 0 == fw_ll.sum(0, 0)

    @pytest.mark.skip(reason="TODO: support modint")
    def test_Zero2(self) -> None:
        fw_modint = ...(0)
        assert 0 == fw_modint.sum(0, 0).val()


@pytest.mark.skip(reason="TODO: support ull")
def test_OverFlowULL() -> None:
    fw = ...(10)
    for i in range(10):
        fw.add(i, (1 << 63) + i)

    for i in range(11):
        for j in range(i, 11):
            sum_ = sum(range(i, j))
            assert ((1 << 63) + sum_ if ((j - i) % 2) else sum_) == fw.sum(i, j)


def test_NaiveTest() -> None:
    for n in range(51):
        fw = fenwick_tree(n)
        for i in range(n):
            fw.add(i, i * i)
        for l in range(n + 1):
            for r in range(l, n + 1):
                sum_ = sum(i * i for i in range(l, r))
                assert sum_ == fw.sum(l, r)


@pytest.mark.skip(reason="TODO: support modint")
def test_SMintTest() -> None:
    # use modint998244353, because cannot specify mod of static_modint
    mint = modint998244353
    for n in range(51):
        fw = ...(n)
        for i in range(n):
            fw.add(i, i * i)
        for l in range(n + 1):
            for r in range(l, n + 1):
                sum_ = mint(0)
                for i in range(l, r):
                    sum_ += i * i
                assert sum_ == fw.sum(l, r)


@pytest.mark.skip(reason="TODO: support modint")
def test_MintTest() -> None:
    mint = modint
    mint.set_mod(11)
    for n in range(51):
        fw = ...(n)
        for i in range(n):
            fw.add(i, i * i)
        for l in range(n + 1):
            for r in range(l, n + 1):
                sum_ = mint(0)
                for i in range(l, r):
                    sum_ += i * i
                assert sum_ == fw.sum(l, r)


class TeseInvalid:
    def test_Invalid1(self) -> None:
        with pytest.raises(ValueError):
            s = fenwick_tree(-1)  # noqa:F841

    @skip_cppassert
    def test_Invalid2(self):
        s = fenwick_tree(10)
        with pytest.raises(AssertionError):
            s.add(-1, 0)
            s.add(10, 0)

            s.sum(-1, 3)
            s.sum(3, 11)
            s.add(5, 3)


class TestBound:
    @pytest.mark.skip(reason="TODO: support int")
    def test_Bound(self) -> None:
        fw = ...
        fw.add(3, numeric_limits("int").max())
        fw.add(5, numeric_limits("int").min())
        assert -1 == fw.sum(0, 10)
        assert -1 == fw.sum(3, 6)
        assert numeric_limits("int").max() == fw.sum(3, 4)
        assert numeric_limits("int").min() == fw.sum(4, 10)

    def test_Boundll(self) -> None:
        fw = fenwick_tree(10)
        fw.add(3, numeric_limits("ll").max())
        fw.add(5, numeric_limits("ll").min())
        assert -1 == fw.sum(0, 10)
        assert -1 == fw.sum(3, 6)
        assert numeric_limits("ll").max() == fw.sum(3, 4)
        assert numeric_limits("ll").min() == fw.sum(4, 10)


@pytest.mark.skip(reason="TODO: support int")
def test_OverFlow() -> None:
    fw = ...(20)
    a = [0] * 20
    for i in range(10):
        x = numeric_limits("int").max()
        a[i] += x
        fw.add(i, x)

    for i in range(10, 20):
        x = numeric_limits("int").min()
        a[i] += x
        fw.add(i, x)

    a[5] += 11111
    fw.add(5, 11111)

    for l in range(21):
        for r in range(l, 21):
            sum_ = sum(a[l:r])
            dif = sum_ - fw.sum(l, r)
            assert 0 == dif % (1 << 32)


@pytest.mark.skip(reason="support __int128?")
def test_Int128() -> None:
    fw = ...(20)
    for i in range(20):
        fw.add(i, i)

    for l in range(21):
        for r in range(l, 21):
            sum_ = sum(range(l, r))
            assert sum_ == fw.sum(l, r)
