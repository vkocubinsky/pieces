"""Module work with prime series.

Prime table is a list of primes which not exceeds `limit` property.

Prime table can be extended explicitly with `extend` method or implicitly
with other methods which require list of primes. 

>>> primes(10)
[2, 3, 5, 7]

>>> is_prime(5)
True

>>> pi(10)
4
"""

import bisect
import logging
import math

from pieces.checks import check_non_negative

__all__ = ["is_prime", "primes", "pi", "extends_prime_table", "reset_prime_table"]


class PrimeTable:
    def __init__(self):
        self.reset()

    @property
    def limit(self) -> int:
        """For number `limit` the class contains prime numbers which not exceeds
        `limit`.
        """
        return self._limit

    def extends(self, n: int):
        """Extends if necessary prime table to table with primes which not exceeds `n`.

        Use Eratosthenes sieve for calculate primes not exceeds n. Primes cached
        in the class instance.
        """
        check_non_negative(n)
        if n > self.limit:
            self._primes = self._calculate(n)
            self._limit = n

    def reset(self):
        """Reset prime table to empty."""
        self._limit = 0
        self._primes = []

    def primes(self, n: int) -> list[int]:
        """Returns list of primes which not exceeds `n`.

        Auto extends if necessary list of primes up to `n`.
        If `n is None` returns all cached primes.

        """
        self.extends(n)
        left = bisect.bisect_right(self._primes, n)
        return self._primes[0:left]

    def pi(self, x: float):
        """Number of prime numbers which not exceeds `x`.

        Auto extends if necessary list of primes up to `floor(x)`.

        Link: [Prime-counting function](https://en.wikipedia.org/wiki/Prime-counting_function).
        """
        n = 0 if x < 0 else math.floor(x)
        self.extends(n)
        i = bisect.bisect_right(self._primes, n)
        return i

    def is_prime(self, n: int):
        """Check  given `n` is a prime.

        Auto extends if necessary list of primes up to `n`.
        """
        self.extends(n)
        i = bisect.bisect_left(self._primes, n)
        if i != len(self._primes) and self._primes[i] == n:
            return True
        else:
            return False

    def _calculate(self, n: int):
        logging.info(f"Recalculate prime tables up to {n}")
        return sieve(n)


def sieve(n: int):
    """For given `n` returns list of primes which not exceeds `n`.

    >>> sieve(10)
    [2, 3, 5, 7]

    Implemented as Sieve of Eratosthene. For performance reason implementation used numpy.
    """
    # Array `a` after initialization looks as
    # [False, False, True, True, True, ... , True]
    # `a[p]` means does `p` is prime
    a = [x >= 2 for x in range(0, n + 1)]
    p = 2
    while p * p <= n:
        if a[p]:
            # Optimization: if p is odd (p*p + p),(p*p + 3p),... is even
            # and was mark as False with p = 2. So we can go with step 2p
            for i in range(p * p, n + 1, p if p == 2 else 2 * p):
                a[i] = False
        p += 1
    return [i for i, v in enumerate(a) if v]


_ptable = PrimeTable()


is_prime = _ptable.is_prime
primes = _ptable.primes
pi = _ptable.pi
extends_prime_table = _ptable.extends
reset_prime_table = _ptable.reset
