class numeric_limits:
    def __init__(self, type_: str) -> None:
        if type_ == "int":
            self.bit_wise = 31
        elif type_ == "ll":
            self.bit_wise = 63
        elif type_ == "uint":
            self.bit_wise = 32
        elif type_ == "ull":
            self.bit_wise = 64
        else:
            raise ValueError

    def max(self):
        return 2 ** (self.bit_wise) - 1

    def min(self):
        return -(2**self.bit_wise)
