from atcoder.dsu import dsu


def test_Zero():
    uf = dsu(0)
    assert [] == uf.groups()


def test_Empty():
    uf = dsu()
    assert [] == uf.groups()


def test_Assign():
    uf = dsu()
    uf = dsu(10)  # noqa:F841


def test_Simple():
    uf = dsu(2)
    assert not uf.same(0, 1)
    x = uf.mearge(0, 1)
    assert x == uf.leader(0)
    assert x == uf.leader(1)
    assert uf.same(0, 1)
    assert 2 == uf.size(0)


def test_Line():
    n = 50000
    uf = dsu(n)
    for i in range(n - 1):
        uf.mearge(i, i + 1)
    assert n == uf.size(0)
    assert 1 == len(uf.groups())


def test_LineReverse():
    n = 50000
    uf = dsu(n)
    for i in reversed(range(n - 1)):
        uf.mearge(i, i + 1)
    assert n == uf.size(0)
    assert 1 == len(uf.groups())
