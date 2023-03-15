def check_bounds(n: int, lower: int, upper: int):
    if not lower <= n <= upper:
        raise ValueError(f"Expected {lower=} <= {n=} <= {upper=} ")


def check_positive(n: int):
    if not n > 0:
        raise ValueError(f"Expected {n=} > 0")


def check_non_negative(n: int):
    if not n >= 0:
        raise ValueError(f"Expected {n=} >= 0")
