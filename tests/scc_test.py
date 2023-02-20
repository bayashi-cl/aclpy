import pytest

from atcoder.scc import scc_graph

from .utils.marker import skip_cppassert


def test_Empty() -> None:
    graph0 = scc_graph()
    assert [] == graph0.scc()
    graph1 = scc_graph(0)
    assert [] == graph1.scc()


def test_Assign() -> None:
    graph = scc_graph()
    graph = scc_graph(10)  # noqa:F841


def test_Simple() -> None:
    graph = scc_graph(2)
    graph.add_edge(0, 0)
    graph.add_edge(0, 0)
    graph.add_edge(1, 1)
    scc = graph.scc()
    assert 2 == len(scc)


@skip_cppassert
def test_Invalid() -> None:
    graph = scc_graph(2)
    with pytest.raises(AssertionError):
        graph.add_edge(0, 10)
