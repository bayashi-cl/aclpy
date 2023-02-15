from typing import overload

class mf_graph:
    def __init__(self, n: int = 0) -> None: ...
    def add_edge(self, from_: int, to: int, cap: int) -> int: ...

    class edge:
        from_: int
        to: int
        cap: int
        flow: int
    def get_edge(self, i: int) -> edge: ...
    def edges(self) -> list[edge]: ...
    def change_edge(self, i: int, new_cap: int, new_flow: int) -> None: ...
    @overload
    def flow(self, s: int, t: int) -> int: ...
    @overload
    def flow(self, s: int, t: int, flow_limit: int) -> int: ...
    def min_cut(self, s: int) -> list[bool]: ...