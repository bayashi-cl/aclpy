class dsu:
    def __init__(self, n: int = 0) -> None: ...
    def mearge(self, a: int, b: int) -> int: ...
    def same(self, a: int, b: int) -> bool: ...
    def leader(self, a: int) -> int: ...
    def size(self, a: int) -> int: ...
    def groups(self) -> list[list[int]]: ...