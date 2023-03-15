from functools import cached_property, total_ordering
from itertools import product
from typing import Iterable

from pieces.ntheory.factorization import defactorize, factorize

__all__ = ["normalize", "Canon"]


def normalize(prime_powers: dict[int, int]) -> dict[int, int]:
    """Normalize prime_powers dict.

    * Keep only items with key(primary number) > 1 and with value(power) > 0.
    * Sort keys

    """
    return {
        k: prime_powers[k]
        for k in sorted(prime_powers.keys())
        if prime_powers[k] > 0 and k > 1
    }


@total_ordering
class Canon:
    def __init__(self, prime_powers: dict[int, int]):
        self._prime_powers = normalize(prime_powers)

    def __getitem__(self, prime):
        """Get power for given *prime*."""
        if prime in self._prime_powers:
            return self._prime_powers[prime]
        else:
            return 0

    def __contains__(self, prime):
        """Check given *prime* in this number."""
        return prime in self._prime_powers

    def primes(self):
        """Return primes for the instance."""
        return self._prime_powers.keys()

    def powers(self):
        """Return powers for the instance in the same order as :meth:`primes`."""
        return self._prime_powers.values()

    def prime_powers(self):
        """Return sequence of (prime, power) for the instance."""
        return self._prime_powers.items()

    @cached_property
    def int_value(self):
        """Integer value for the instance representation"""
        return defactorize(self._prime_powers)

    def divisors(self) -> Iterable["Canon"]:
        """Returns divisors of the instance."""
        primes, powers = self.primes(), self.powers()
        product_of_powers = product(*(range(0, power + 1) for power in powers))
        return [
            Canon(dict(zip(primes, comb_powers))) for comb_powers in product_of_powers
        ]

    def is_unit(self) -> bool:
        """Is the instance representation of 1."""
        return not bool(self._prime_powers)

    def is_prime_power(self) -> bool:
        """Returns true if the instance is power of prime, otherwise return false."""
        return len(self._prime_powers) == 1

    def is_composite(self) -> bool:
        """Returns true if the instance is a composite number, otherwise return false."""
        return not self.is_unit() and not self.is_prime()

    def is_prime(self) -> bool:
        """Returns true if the instance is a prime, otherwise return false."""
        return (
            len(self._prime_powers) == 1 and list(self._prime_powers.values())[0] == 1
        )

    def is_divides(self, divisor: "Canon") -> bool:
        """Does divisor divide the instance

        Returns:
            True if this number divide to ``divisor`` is integer
        """
        for k, v in divisor.prime_powers():
            if self[k] < v:
                return False
        return True

    def __mul__(self, other: "Canon"):
        if not isinstance(other, Canon):
            return NotImplemented

        return Canon({k: self[k] + other[k] for k in self.primes() | other.primes()})

    def __pow__(self, power):
        if isinstance(power, int) and power >= 0:
            return Canon({k: v * power for k, v in self._prime_powers.items()})
        else:
            return NotImplemented

    def __truediv__(self, other: "Canon"):
        if not isinstance(other, Canon):
            return NotImplemented

        if self.is_divides(other):
            return Canon(
                {k: self[k] - other[k] for k in self.primes() | other.primes()}
            )
        else:
            raise ArithmeticError(f"Canon {self} is not divisible by {other}")

    def __lt__(self, other):
        return self.int_value < other.int_value

    def __eq__(self, other):
        return other is not None and self.int_value == other.int_value

    def __int__(self):
        return self.int_value

    def __repr__(self):
        return f"Canon({self._prime_powers!r})"

    def __str__(self):
        return str(self._prime_powers)

    @staticmethod
    def factorize(n: int) -> "Canon":
        prime_powers = factorize(n)
        return Canon(prime_powers)
