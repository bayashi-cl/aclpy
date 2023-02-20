from random import randint


def randbool():
    return randint(0, 1) == 0


def randpair(lower: int, upper: int) -> tuple[int, int]:
    assert upper - lower >= 1
    a, b = 0, 0
    while a == b:
        a = randint(lower, upper)
        b = randint(lower, upper)

    if a > b:
        a, b = b, a
    return (a, b)
