from random import randint

import pytest

from atcoder.maxflow import mf_graph
from atcoder.mincostflow import mcf_graph

from .utils.marker import skip_cppassert
from .utils.random_ import randbool, randpair


def test_Zero() -> None:
    g1 = mcf_graph()  # noqa:F841
    g1 = mcf_graph(0)  # noqa:F841


def edge_eq(expect: mcf_graph.edge, actual: mcf_graph.edge) -> None:
    assert expect.from_ == actual.from_
    assert expect.to == actual.to
    assert expect.cap == actual.cap
    assert expect.flow == actual.flow
    assert expect.cost == actual.cost


def test_Simple() -> None:
    g = mcf_graph(4)
    g.add_edge(0, 1, 1, 1)
    g.add_edge(0, 2, 1, 1)
    g.add_edge(1, 3, 1, 1)
    g.add_edge(2, 3, 1, 1)
    g.add_edge(1, 2, 1, 1)
    expect = [(0, 0), (2, 4)]
    assert expect == g.slope(0, 3, 10)
    e = mcf_graph.edge()

    e.from_, e.to, e.cap, e.flow, e.cost = 0, 1, 1, 1, 1
    edge_eq(e, g.get_edge(0))
    e.from_, e.to, e.cap, e.flow, e.cost = 0, 2, 1, 1, 1
    edge_eq(e, g.get_edge(1))
    e.from_, e.to, e.cap, e.flow, e.cost = 1, 3, 1, 1, 1
    edge_eq(e, g.get_edge(2))
    e.from_, e.to, e.cap, e.flow, e.cost = 2, 3, 1, 1, 1
    edge_eq(e, g.get_edge(3))
    e.from_, e.to, e.cap, e.flow, e.cost = 1, 2, 1, 0, 1
    edge_eq(e, g.get_edge(4))


class TestUsage:
    def test_Usage1(self) -> None:
        g = mcf_graph(2)
        g.add_edge(0, 1, 1, 2)
        assert (1, 2) == g.flow(0, 1)

    def test_Usage2(self) -> None:
        g = mcf_graph(2)
        g.add_edge(0, 1, 1, 2)
        expect = [(0, 0), (1, 2)]
        assert expect == g.slope(0, 1)


def test_Assign() -> None:
    g = mcf_graph()
    g = mcf_graph(10)  # noqa:F841


@skip_cppassert
def test_OutOfRange() -> None:
    g = mcf_graph(10)
    with pytest.raises(AssertionError):
        g.slope(-1, 3)
        g.slope(3, 3)


def test_SelfLoop() -> None:
    g = mcf_graph(3)
    assert 0 == g.add_edge(0, 0, 100, 123)

    e = mcf_graph.edge()
    e.from_, e.to, e.cap, e.flow, e.cost = 0, 0, 100, 0, 123
    edge_eq(e, g.get_edge(0))


def test_SameCostPaths() -> None:
    g = mcf_graph(3)
    assert 0 == g.add_edge(0, 1, 1, 1)
    assert 1 == g.add_edge(1, 2, 1, 0)
    assert 2 == g.add_edge(0, 2, 2, 1)
    expected = [(0, 0), (3, 3)]
    assert expected == g.slope(0, 2)


@skip_cppassert
def test_Invaid() -> None:
    g = mcf_graph(2)
    with pytest.raises(AssertionError):
        g.add_edge(0, 0, -1, 0)
        g.add_edge(0, 0, 0, -1)


def test_Stress() -> None:
    for _ in range(1000):
        n = randint(2, 20)
        m = randint(1, 100)
        s, t = randpair(0, n - 1)
        if randbool():
            s, t = t, s

        g_mf = mf_graph(n)
        g = mcf_graph(n)
        for i in range(m):
            u = randint(0, n - 1)
            v = randint(0, n - 1)
            cap = randint(0, 10)
            cost = randint(0, 10000)
            g.add_edge(u, v, cap, cost)
            g_mf.add_edge(u, v, cap)
        flow, cost = g.flow(s, t)
        assert g_mf.flow(s, t) == flow

        cost2 = 0
        v_cap = [0] * n
        for e in g.edges():
            v_cap[e.from_] -= e.flow
            v_cap[e.to] += e.flow
            cost2 += e.flow * e.cost
        assert cost == cost2

        for i in range(n):
            if i == s:
                assert -flow == v_cap[i]
            elif i == t:
                assert flow == v_cap[i]
            else:
                assert 0 == v_cap[i]

        # check: there is no negative-cycle
        dist = [0] * n
        while True:
            update = False
            for e in g.edges():
                if e.flow < e.cap:
                    ndist = dist[e.from_] + e.cost
                    if ndist < dist[e.to]:
                        update = True
                        dist[e.to] = ndist
                if e.flow:
                    ndist = dist[e.to] - e.cost
                    if ndist < dist[e.from_]:
                        update = True
                        dist[e.from_] = ndist
            if not update:
                break
