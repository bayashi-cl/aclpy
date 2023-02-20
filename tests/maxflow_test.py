from random import randint

import pytest

from atcoder.maxflow import mf_graph

from .utils.limits import numeric_limits
from .utils.marker import skip_cppassert
from .utils.random_ import randbool, randpair


def test_Zero() -> None:
    g1 = mf_graph()  # noqa:F841
    g2 = mf_graph(0)  # noqa:F841


def test_Assign() -> None:
    g = mf_graph()
    g = mf_graph(10)  # noqa:F841


def edge_eq(expect: mf_graph.edge, actual: mf_graph.edge) -> None:
    assert expect.from_ == actual.from_
    assert expect.to == actual.to
    assert expect.cap == actual.cap
    assert expect.flow == actual.flow


def test_Simple() -> None:
    g = mf_graph(4)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 2, 1)
    assert 2 == g.add_edge(1, 3, 1)
    assert 3 == g.add_edge(2, 3, 1)
    assert 4 == g.add_edge(1, 2, 1)
    assert 2 == g.flow(0, 3)

    e = mf_graph.edge()
    e.from_, e.to, e.cap, e.flow = 0, 1, 1, 1
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 0, 2, 1, 1
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow = 1, 3, 1, 1
    edge_eq(e, g.get_edge(2))
    e.from_, e.to, e.cap, e.flow = 2, 3, 1, 1
    edge_eq(e, g.get_edge(3))
    e.from_, e.to, e.cap, e.flow = 1, 2, 1, 0
    edge_eq(e, g.get_edge(4))

    assert [True, False, False, False] == g.min_cut(0)


def test_NotSimple() -> None:
    g = mf_graph(2)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 1, 2)
    assert 2 == g.add_edge(0, 1, 3)
    assert 3 == g.add_edge(0, 1, 4)
    assert 4 == g.add_edge(0, 1, 5)
    assert 5 == g.add_edge(0, 0, 6)
    assert 6 == g.add_edge(1, 1, 7)
    assert 15 == g.flow(0, 1)

    e = mf_graph.edge()
    e.from_, e.to, e.cap, e.flow = 0, 1, 1, 1
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 0, 1, 2, 2
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow = 0, 1, 3, 3
    edge_eq(e, g.get_edge(2))
    e.from_, e.to, e.cap, e.flow = 0, 1, 4, 4
    edge_eq(e, g.get_edge(3))
    e.from_, e.to, e.cap, e.flow = 0, 1, 5, 5
    edge_eq(e, g.get_edge(4))


def test_Cut() -> None:
    g = mf_graph(3)
    assert 0 == g.add_edge(0, 1, 2)
    assert 1 == g.add_edge(1, 2, 1)
    assert 1 == g.flow(0, 2)

    e = mf_graph.edge()
    e.from_, e.to, e.cap, e.flow = 0, 1, 2, 1
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 1, 2, 1, 1
    edge_eq(e, g.get_edge(1))

    assert [True, True, False] == g.min_cut(0)


def test_Twice() -> None:
    e = mf_graph.edge()

    g = mf_graph(3)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 2, 1)
    assert 2 == g.add_edge(1, 2, 1)

    assert 2 == g.flow(0, 2)

    e.from_, e.to, e.cap, e.flow = 0, 1, 1, 1
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 0, 2, 1, 1
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow = 1, 2, 1, 1
    edge_eq(e, g.get_edge(2))

    g.change_edge(0, 100, 10)
    e.from_, e.to, e.cap, e.flow = 0, 1, 100, 10
    edge_eq(e, g.get_edge(0))

    assert 0 == g.flow(0, 2)
    assert 90 == g.flow(0, 1)

    e.from_, e.to, e.cap, e.flow = 0, 1, 100, 100
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 0, 2, 1, 1
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow = 1, 2, 1, 1
    edge_eq(e, g.get_edge(2))

    assert 2 == g.flow(2, 0)

    e.from_, e.to, e.cap, e.flow = 0, 1, 100, 99
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow = 0, 2, 1, 0
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow = 1, 2, 1, 0
    edge_eq(e, g.get_edge(2))


class TestBound:
    def test_Bound(self) -> None:
        e = mf_graph.edge()

        INF = numeric_limits("int").max()
        g = mf_graph(3)
        assert 0 == g.add_edge(0, 1, INF)
        assert 1 == g.add_edge(1, 0, INF)
        assert 2 == g.add_edge(0, 2, INF)

        assert INF == g.flow(0, 2)

        e.from_, e.to, e.cap, e.flow = 0, 1, INF, 0
        edge_eq(e, g.get_edge(0))
        e.from_, e.to, e.cap, e.flow = 1, 0, INF, 0
        edge_eq(e, g.get_edge(1))
        e.from_, e.to, e.cap, e.flow = 0, 2, INF, INF
        edge_eq(e, g.get_edge(2))

    @pytest.mark.skip(reason="support uint")
    def test_BoundUint(self) -> None:
        e = ....edge()

        INF = numeric_limits("int").max()
        g = ...(3)
        assert 0 == g.add_edge(0, 1, INF)
        assert 1 == g.add_edge(1, 0, INF)
        assert 2 == g.add_edge(0, 2, INF)

        assert INF == g.flow(0, 2)

        e.from_, e.to, e.cap, e.flow = 0, 1, INF, 0
        edge_eq(e, g.get_edge(0))
        e.from_, e.to, e.cap, e.flow = 1, 0, INF, 0
        edge_eq(e, g.get_edge(1))
        e.from_, e.to, e.cap, e.flow = 0, 2, INF, INF
        edge_eq(e, g.get_edge(2))


def test_SelfLoop() -> None:
    g = mf_graph(3)
    assert 0 == g.add_edge(0, 0, 100)

    e = mf_graph.edge()
    e.from_, e.to, e.cap, e.flow = 0, 0, 100, 0
    edge_eq(e, g.get_edge(0))


@skip_cppassert
def test_Invalid() -> None:
    g = mf_graph(2)
    with pytest.raises(AssertionError):
        g.flow(0, 0)
        g.flow(0, 0, 0)


def test_Stress() -> None:
    for _ in range(10000):
        n = randint(2, 20)
        m = randint(1, 100)
        s, t = randpair(0, n - 1)
        if randbool():
            s, t = t, s

        g = mf_graph(n)
        for _ in range(m):
            u = randint(0, n - 1)
            v = randint(0, n - 1)
            c = randint(0, 10000)
            g.add_edge(u, v, c)
        flow = g.flow(s, t)
        dual = 0
        cut = g.min_cut(s)
        v_flow = [0] * n
        for e in g.edges():
            v_flow[e.from_] -= e.flow
            v_flow[e.to] += e.flow
            if cut[e.from_] and not cut[e.to]:
                dual += e.cap
        assert flow == dual
        assert -flow == v_flow[s]
        assert flow == v_flow[t]
        for i in range(n):
            if i == s or i == t:
                continue
            assert 0 == v_flow[i]
