import pytest

from atcoder.string import lcp_array, suffix_array, z_algorithm

from .utils.limits import numeric_limits


def sa_naive(s: list[int]) -> list[int]:
    n = len(s)
    sa = list(range(n))
    sa.sort(key=lambda x: s[x:])
    return sa


def lcp_naive(s: list[int], sa: list[int]) -> list[int]:
    n = len(s)
    assert n
    lcp = [0] * (n - 1)
    for i in range(n - 1):
        l = sa[i]
        r = sa[i + 1]
        while l + lcp[i] < n and r + lcp[i] < n and s[l + lcp[i]] == s[r + lcp[i]]:
            lcp[i] += 1
    return lcp


def z_naive(s: list[int]) -> list[int]:
    n = len(s)
    z = [0] * n
    for i in range(n):
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
    return z


def test_Empty() -> None:
    assert [] == suffix_array("")
    assert [] == suffix_array([])

    assert [] == z_algorithm("")
    assert [] == z_algorithm([])


@pytest.mark.parametrize(("max_n", "k"), [(5, 4), (10, 2)])
def test_SALCPNaive(max_n: int, k: int) -> None:
    for n in range(1, max_n + 1):
        m = k**n
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % k
                max_c = max(max_c, s[i])
                g //= k
            sa = sa_naive(s)
            assert sa == suffix_array(s)
            assert sa == suffix_array(s, max_c)
            assert lcp_naive(s, sa) == lcp_array(s, sa)


@pytest.mark.skip(reason="internal")
def test_InternalSANaiveNaive() -> None:
    pass


@pytest.mark.skip(reason="internal")
def test_InternalSADoublingNaive() -> None:
    pass


@pytest.mark.skip(reason="internal")
def test_InternalSAISNaive() -> None:
    pass


def test_SAAllATest() -> None:
    for n in range(1, 101):
        s = [10] * n
        assert sa_naive(s) == suffix_array(s)
        assert sa_naive(s) == suffix_array(s, 10)
        assert sa_naive(s) == suffix_array(s, 12)


def test_SAAllABTest() -> None:
    for n in range(1, 101):
        s = [0] * n
        for i in range(n):
            s[i] = i % 2
        assert sa_naive(s) == suffix_array(s)
        assert sa_naive(s) == suffix_array(s, 3)

    for n in range(1, 101):
        s = [0] * n
        for i in range(n):
            s[i] = 1 - (i % 2)
        assert sa_naive(s) == suffix_array(s)
        assert sa_naive(s) == suffix_array(s, 3)


def test_SA() -> None:
    s = "missisippi"
    sa = suffix_array(s)
    answer = [
        "i",  # 9
        "ippi",  # 6
        "isippi",  # 4
        "issisippi",  # 1
        "missisippi",  # 0
        "pi",  # 8
        "ppi",  # 7
        "sippi",  # 5
        "sisippi",  # 3
        "ssisippi",  # 2
    ]

    assert len(answer) == len(sa)
    for i in range(len(sa)):
        assert answer[i] == s[sa[i] :]


def test_SASingle() -> None:
    assert [0] == suffix_array([0])
    assert [0] == suffix_array([-1])
    assert [0] == suffix_array([1])
    assert [0] == suffix_array([numeric_limits("int").min()])
    assert [0] == suffix_array([numeric_limits("int").max()])


def test_LCP() -> None:
    s = "aab"
    sa = suffix_array(s)
    assert [0, 1, 2] == sa
    lcp = lcp_array(s, sa)
    assert [1, 0] == lcp

    assert lcp == lcp_array([0, 0, 1], sa)
    assert lcp == lcp_array([-100, -100, 100], sa)
    assert lcp == lcp_array(
        [
            numeric_limits("int").min(),
            numeric_limits("int").min(),
            numeric_limits("int").max(),
        ],
        sa,
    )
    assert lcp == lcp_array(
        [
            numeric_limits("ll").min(),
            numeric_limits("ll").min(),
            numeric_limits("ll").max(),
        ],
        sa,
    )
    assert lcp == lcp_array(
        [
            numeric_limits("uint").min(),
            numeric_limits("uint").min(),
            numeric_limits("uint").max(),
        ],
        sa,
    )
    # skip: ull::max() > sys.maxsize
    # assert lcp == lcp_array(
    #     [
    #         numeric_limits("ull").min(),
    #         numeric_limits("ull").min(),
    #         numeric_limits("ull").max(),
    #     ],
    #     sa,
    # )


def test_ZAlgo() -> None:
    s = "abab"
    z = z_algorithm(s)
    assert [4, 0, 2, 0] == z
    assert [4, 0, 2, 0] == z_algorithm([1, 10, 1, 10])
    assert z_naive([0, 0, 0, 0, 0, 0, 0]) == z_algorithm([0, 0, 0, 0, 0, 0, 0])


@pytest.mark.parametrize(("max_n", "k"), [(6, 4), (10, 2)])
def test_ZNaive(max_n: int, k: int) -> None:
    for n in range(1, max_n + 1):
        m = k**n
        for f in range(m):
            s = [0] * n
            g = f
            for i in range(n):
                s[i] = g % k
                g //= k
            assert z_naive(s) == z_algorithm(s)
