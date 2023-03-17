"""Arithmetical functions."""
import itertools
import math
from enum import Enum, auto
from numbers import Real
from pieces.checks import check_positive

from pieces.ntheory.canon import Canon

__all__ = [
    "divisors",
    "mobius",
    "totient",
    "totient_inverse",
    "little_omega",
    "big_omega",
    "d",
    "sigma",
    "N",
    "identity",
    "unit",
    "liouville",
    "mangoldt",
]

from abc import ABC, abstractmethod

EQ_SIZE = 100


class Category(Enum):
    multiplicative = auto()
    additive = auto()
    completely_multiplicative = auto()
    completely_additive = auto()
    neither_multiplicative_nor_additive = auto()


def divisors(n) -> list[int]:
    return [x.int_value for x in Canon.factorize(n).divisors()]


def lcm(a: Canon, b: Canon) -> Canon:
    """Least common multiple of two numbers in canonical form.

    >>> lcm(Canon.factorize(18), Canon.factorize(12)).int_value
    36

    """
    return Canon({k: max(a[k], b[k]) for k in a.primes() | b.primes()})


def gcd(a: Canon, b: Canon) -> Canon:
    """Greatest common divisor of two number in canonical form.

    Example:
    >>> gcd(Canon.factorize(18), Canon.factorize(12)).int_value
    6
    """
    return Canon({k: min(a[k], b[k]) for k in a.primes() | b.primes()})


class ArithmeticFunction(ABC):
    """Base class for arithmetic function."""

    def __init__(self):
        self.category = Category.neither_multiplicative_nor_additive

    @property
    def multiplicative(self):
        return self.category in (
            Category.multiplicative,
            Category.completely_multiplicative,
        )

    @property
    def additive(self):
        return self.category in (Category.additive, Category.completely_additive)

    @property
    def completely_multiplicative(self):
        return self.category == Category.completely_multiplicative

    @property
    def completely_additive(self):
        return self.category == Category.completely_additive

    def __str__(self):
        return self.formula

    @property
    @abstractmethod
    def formula(self) -> str:
        ...

    def __call__(self, n: int | Canon) -> Real:
        match n:
            case Canon():
                return self.call_on_canon(n)
            case int():
                return self.call_on_int(n)
            case _:
                raise NotImplementedError(f"Not implemented for type {type(n)}")

    @abstractmethod
    def call_on_canon(self, canon: Canon) -> Real:
        ...

    def call_on_int(self, n: int) -> Real:
        return self.call_on_canon(Canon.factorize(n))

    def __eq__(self, other: "ArithmeticFunction"):
        if id(self) == id(other):
            return True
        for x in range(1, EQ_SIZE):
            if self(x) != other(x):
                return False
        return True

    def __mul__(self, g) -> "ArithmeticFunction":
        """Special methods which returns dirichlet product this function multiply by `g`.

        So we can write f*g for dirichlet product.
        """
        return DirichletProduct(self, g)

    def inverse(self) -> "ArithmeticFunction":
        """Dirichlet inverse."""
        if self.completely_multiplicative:
            return PointwiseProduct(mobius, self)
        else:
            return DirichletInverse(self)

    def __pow__(self, power):
        if power >= 0:
            return math.prod(itertools.repeat(self, power), start=identity)
        else:
            return math.prod(itertools.repeat(self.inverse(), -power), start=identity)


class DirichletInverse(ArithmeticFunction):
    def __init__(self, f):
        super().__init__()
        self.f = f
        if f.multiplicative:
            self.category = Category.multiplicative

    def call_on_canon(self, canon: Canon) -> Real:
        return self.invert(canon)

    def invert(self, n: Canon) -> Real:
        if n.int_value == 1:
            return 1 / n.int_value
        else:
            return (
                -1
                / self.f(1)
                * sum([self.f(n / d) * self.invert(d) for d in n.divisors() if d < n])
            )

    @property
    def formula(self) -> str:
        return f"{self.f.formula}⁻¹"

    def inverse(self) -> ArithmeticFunction:
        return self.f


class PointwiseProduct(ArithmeticFunction):
    """Pointwise products of two functions.

    Pointwise product of two arithmetic functions `f` and `g` is defined as usual
    function multiplication:
    ```
    (f ∙ g)(n) = f(n) * g(n)
    ```
    """

    def __init__(self, f: ArithmeticFunction, g: ArithmeticFunction):
        super().__init__()
        self.f = f
        self.g = g

    def call_on_canon(self, canon: Canon) -> Real:
        return self.f(canon) * self.g(canon)

    def call_on_int(self, n: int) -> Real:
        return self.f(n) * self.g(n)

    @property
    def formula(self) -> str:
        return f"{self.f.formula} ∙ {self.g.formula}"


class DirichletProduct(ArithmeticFunction):
    r"""Dirichlet product.

    Dirichlet product of two arithmetic functions defined as
    ```
    (f * g)(n) = sum(f(d) * g(n/d) : d \ n )
    ```
    """

    def __init__(self, f: ArithmeticFunction, g: ArithmeticFunction):
        super().__init__()
        self.f = f
        self.g = g
        if f.completely_multiplicative and g.completely_multiplicative:
            self.category = Category.completely_multiplicative
        elif f.multiplicative and g.multiplicative:
            self.category = Category.multiplicative
        else:
            self.category = Category.neither_multiplicative_nor_additive

    def call_on_canon(self, n: Canon) -> Real:
        return sum((self.f(d) * self.g(n / d) for d in n.divisors()))

    def inverse(self) -> ArithmeticFunction:
        return (self.f ** -1) * (self.g ** -1)

    @property
    def formula(self) -> str:
        return f"{self.f} * {self.g}"


class AdditiveFunction(ArithmeticFunction):
    r"""Base class for additive arithmetic function.

    ```
    f(m * n) = f(m) + f(n) if m and n relative prime
    ```
    """

    def __init__(self):
        super().__init__()
        self.category = Category.additive

    def call_on_canon(self, canon: Canon):
        return sum([self.call_on_prime(p, k) for p, k in canon.prime_powers()])

    @abstractmethod
    def call_on_prime(self, prime: int, power: int):
        """Called for prime > 1 and power > 0"""
        raise NotImplementedError


class MultiplicativeFunction(ArithmeticFunction):
    """Abstract base class for Multiplicative Function"""

    def call_on_canon(self, canon: Canon):
        return math.prod(
            [self.call_on_prime(prime, power) for prime, power in canon.prime_powers()]
        )

    @abstractmethod
    def call_on_prime(self, prime: int, power: int):
        """Called for prime > 1 and power > 0"""
        raise NotImplementedError


class DistinctPrimesFunction(AdditiveFunction):
    r"""Count of distinct primes divides given `n`.

    Distinct primes is additive function. This function can be defined on prime
    powers as

    ```
    ω(p^k) = 1
    ```

    >>> little_omega(2**5 * 3 **2 * 7) # 1 + 1 + 1
    3
    """

    def call_on_prime(self, prime: int, power: int):
        return 1

    @property
    def formula(self) -> str:
        return "ω"


little_omega = DistinctPrimesFunction()


class TotalPrimesFunction(AdditiveFunction):
    r"""Total count of primes with their multiplicity divides given `n`.

    Total primes is completely additive function. This function can be defined
    on prime powers as

    ```
    Ω(p^k) = k

    ```
    >>> big_omega(2**3 * 5**2) # 3 + 2
    5
    """

    def __init__(self):
        super().__init__()
        self.category = Category.completely_additive

    def call_on_prime(self, prime: int, power: int):
        return power

    @property
    def formula(self) -> str:
        return "Ω"


big_omega = TotalPrimesFunction()


class TotientFunction(MultiplicativeFunction):
    """Euler's totient function.

    Euler's totient function is multiplicative function. This function can be
    defined on prime powers as

    ```
    φ(p^k) = p^k - p^(k-1)
    ```

    >>> totient(10)
    4
    """

    def call_on_prime(self, prime, power):
        return prime ** (power - 1) * (prime - 1)

    def inverse(self):
        return totient_inverse

    @property
    def formula(self) -> str:
        return "φ"


totient = TotientFunction()


class TotientInverseFunction(MultiplicativeFunction):
    def call_on_prime(self, prime, power):
        return 1 - prime

    def inverse(self):
        return totient

    @property
    def formula(self) -> str:
        return "φ⁻¹"


totient_inverse = TotientInverseFunction()


class MobiusFunction(MultiplicativeFunction):
    """Mobius function.

    Mobius function is multiplicative function.

    Example:
    >>> mobius(10)
    1
    """

    def call_on_prime(self, _: int, power: int):
        return 0 if power > 1 else -1

    def inverse(self) -> ArithmeticFunction:
        return unit

    @property
    def formula(self) -> str:
        return "μ"


mobius = MobiusFunction()


class PowerFunction(ArithmeticFunction):
    """Function `n ^ k` where `k` is some constant.

    >>> N(5)
    5
    """

    def __init__(self, k: int):
        super().__init__()
        self.k = k
        self.category = Category.completely_multiplicative

    def call_on_int(self, n: int):
        return n**self.k

    def call_on_canon(self, canon: Canon):
        return (canon**self.k).int_value

    @property
    def formula(self) -> str:
        return "N" if self.k == 1 else f"N^{self.k}"


N = PowerFunction(1)


class IdentityFunction(ArithmeticFunction):
    """Identity function I is defined as

    ```
    I(n) =
        | 1 if n = 1
        | 0 if n > 1
    ```

    >>> identity(1)
    1
    >>> identity(5)
    0
    """

    def __init__(self):
        super().__init__()
        self.category = Category.completely_multiplicative

    def call_on_int(self, n: int):
        return 1 if n == 1 else 0

    def call_on_canon(self, canon: Canon):
        return 1 if canon.is_unit() else 0

    def inverse(self):
        return self

    def __mul__(self, g):
        return g

    @property
    def formula(self) -> str:
        return "I"


identity = IdentityFunction()


class UnitFunction(ArithmeticFunction):
    """Unit function.

    Always returns 1
    >>> unit(5)
    1
    """

    def call_on_int(self, n: int):
        return 1

    def call_on_canon(self, canon: Canon):
        return 1

    def inverse(self):
        return mobius

    @property
    def formula(self) -> str:
        return "u"


unit = UnitFunction()


class NumberOfDivisors(MultiplicativeFunction):
    r"""Number of divisor function.

    ```
    d(n) = sum(1 : for all d \ n)
    ```

    Number of divisor function denoted by `d(n)`.
    """
    def call_on_prime(self, prime: int, power: int):
        return power + 1

    @property
    def formula(self):
        return "d"

    def inverse(self) -> "ArithmeticFunction":
        return mobius * mobius

d = NumberOfDivisors()


class DivisorsSumFunction(MultiplicativeFunction):
    r"""Divisors sum function.

    Sum of `k` powers of positive divisors of n.

    ```
    σ(k,n) = sum([d ^ k : for all d \ n])
    ```

    Count of divisors σ(0,n) is denoted as tau(`τ`)

    Sum of divisors σ(0,n) is denoted as sigma(`σ`)

    >>> sigma(6) # 1 + 2 + 3 + 6
    12
    """

    def __init__(self, divisor_power):
        super().__init__()
        self.divisor_power = check_positive(divisor_power)

    def call_on_prime(self, prime: int, power: int):
        pa = prime**self.divisor_power
        return int((pa ** (power + 1) - 1) / (pa - 1))

    @property
    def formula(self) -> str:
        if self.divisor_power == 1:
            return "σ"
        else:
            return f"σ({self.divisor_power})"

sigma = DivisorsSumFunction(1)


class MangoldtFunction(ArithmeticFunction):
    def __init__(self):
        super().__init__()
        self.category = Category.neither_multiplicative_nor_additive

    def call_on_canon(self, canon: Canon):
        if len(canon.primes()) == 1:
            (prime,) = canon.primes()
            return math.log(prime)
        else:
            return 0

    @property
    def formula(self) -> str:
        return "Λ"


mangoldt = MangoldtFunction()  #: pre-built instance of :class:`MangoldtFunction`


class LiouvilleFunction(MultiplicativeFunction):
    def __init__(self):
        super().__init__()
        self.category = Category.completely_multiplicative

    def call_on_prime(self, prime: int, power: int):
        return (-1) ** power

    def inverse(self):
        return mobius * mobius

    @property
    def formula(self) -> str:
        return "λ"


liouville = LiouvilleFunction()
