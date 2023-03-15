"""Low level factorization module.

See: `pieces.ntheory.canon` for high level factorization module.

Example:

>>> from pieces.ntheory import factorize, defactorize
>>> factorize(72)
{2: 3, 3: 2}
>>> defactorize({2: 3, 3: 2})
72

Note: Implementation of `factorize` function use list of primes from
`pieces.ntheory.prime` module. Prime table automatically extended if list of
primes is not enough to factorize given number `n`(require list of prime numbers 
which not exceeds `sqrt(n)`). But extends prime table is not incremental
procedure. For some cases for performance reason have sense to explicitly
extends prime table to avoid automatic extension of prime table list. For
example: 

```
extends_prime_table(1000) # enough for factorize numbers <= 1000 * 1000
[factorize(n) for n in range(1,1_000_000)]
```

"""
import math

from pieces.checks import check_positive
from pieces.ntheory.primes import primes

__all__ = ["factorize", "defactorize", "pvaluation"]


def pvaluation(a: int, p: int):
    """Returns the largest exponent of `p` which divides `a`.

    That is, `p^k` divides a, but p^(k+1) not

    Example:

    >>> pvaluation(2**3 * 35, 2)
    3
    """
    return _div_max_power(a, p)[1]


def _div_max_power(a: int, p: int):
    """Returns a tuple `(a//p^k, k)`, where k is the largest exponent of p which
    divides `a`.

    That is, p^k divides a, but p^(k+1) not.

    Example:

    >>> _div_max_power(2**3 * 35, 2)
    (35, 3)
    """
    k = 0
    while a % p == 0:
        k += 1
        a //= p
    return a, k


def factorize(n: int) -> dict[int, int]:
    """Factorize integer `n`.

    Returns a dict, where key is a prime `p` in `n` and value is a power of `p`
    in `n`. Primes in dict has ascending order, power of primes more than zero.

    >>> factorize(2**3 * 3**2)
    {2: 3, 3: 2}

    Number 1 represented as empty dict.

    >>> factorize(1)
    {}
    """
    check_positive(n)

    prime_powers = {}
    for p in primes(math.isqrt(n)):
        if p * p > n:
            break
        n, power = _div_max_power(n, p)
        if power > 0:
            prime_powers[p] = power

    if n > 1:
        prime_powers[n] = 1

    return prime_powers


def defactorize(prime_powers: dict[int, int]) -> int:
    """Returns integer, whose factorization is `prime_powers`.

    >>> defactorize({2: 3, 3: 2})
    72
    """
    return math.prod([p**m for p, m in prime_powers.items()])
