def check_bounds(n: int, lower: int, upper: int) -> int:
    if not lower <= n <= upper:
        raise ValueError(f"Expected {lower=} <= {n=} <= {upper=} ")
    return n


def check_positive(n: int) -> int:
    if not n > 0:
        raise ValueError(f"Expected {n=} > 0")
    return n


def check_non_negative(n: int) -> int:
    if not n >= 0:
        raise ValueError(f"Expected {n=} >= 0")
    return n
