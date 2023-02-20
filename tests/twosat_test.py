from random import randint

from atcoder.twosat import two_sat

from .utils.random_ import randbool


def test_Empty() -> None:
    ts0 = two_sat()
    assert ts0.satisfiable()
    assert [] == ts0.answer()
    ts1 = two_sat(0)
    assert ts1.satisfiable()
    assert [] == ts1.answer()


class TestOne:
    def test_One1(self) -> None:
        ts = two_sat(1)
        ts.add_clause(0, True, 0, True)
        ts.add_clause(0, False, 0, False)
        assert not ts.satisfiable()

    def test_One2(self) -> None:
        ts = two_sat(1)
        ts.add_clause(0, True, 0, True)
        assert ts.satisfiable()
        assert [True] == ts.answer()

    def test_One3(self) -> None:
        ts = two_sat(1)
        ts.add_clause(0, False, 0, False)
        assert ts.satisfiable()
        assert [False] == ts.answer()


def test_Assign() -> None:
    ts = two_sat()
    ts = two_sat(10)  # noqa:F841


def test_StressOK() -> None:
    for _ in range(10000):
        n = randint(1, 20)
        m = randint(1, 100)
        expect = [randbool() for _ in range(n)]

        ts = two_sat(n)
        xs = [0] * m
        ys = [0] * m
        types = [0] * m
        for i in range(m):
            x = randint(0, n - 1)
            y = randint(0, n - 1)
            type_ = randint(0, 2)
            xs[i] = x
            ys[i] = y
            types[i] = type_
            if type_ == 0:
                ts.add_clause(x, expect[x], y, expect[y])
            elif type_ == 1:
                ts.add_clause(x, not expect[x], y, expect[y])
            else:
                ts.add_clause(x, expect[x], y, not expect[y])
        assert ts.satisfiable()
        actual = ts.answer()
        for i in range(m):
            x = xs[i]
            y = ys[i]
            type_ = types[i]
            if type_ == 0:
                assert actual[x] == expect[x] or actual[y] == expect[y]
            elif type_ == 1:
                assert actual[x] != expect[x] or actual[y] == expect[y]
            else:
                assert actual[x] == expect[x] or actual[y] != expect[y]
