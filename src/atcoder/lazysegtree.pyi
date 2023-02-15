from typing import Callable, Generic, TypeVar, overload

S = TypeVar("S")
F = TypeVar("F")

class lazysegtree(Generic[S, F]):
    @overload
    def __init__(
        self,
        op: Callable[[S, S], S],
        e: Callable[[], S],
        mapping: Callable[[F, S], S],
        composition: Callable[[F, F], F],
        id: Callable[[], F],
        n: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self,
        op: Callable[[S, S], S],
        e: Callable[[], S],
        mapping: Callable[[F, S], S],
        composition: Callable[[F, F], F],
        id: Callable[[], F],
        v: list[int],
    ) -> None: ...
    def set(self, p: int, x: S) -> None: ...
    def get(self, p: int) -> S: ...
    def prod(self, l: int, r: int) -> S: ...
    def all_prod(self) -> S: ...
    @overload
    def apply(self, p: int, f: F) -> None: ...
    @overload
    def apply(self, l: int, r: int, f: F) -> None: ...
    def max_right(self, l: int, g: Callable[[S], bool]) -> int: ...
    def min_left(self, r: int, g: Callable[[S], bool]) -> int: ...
