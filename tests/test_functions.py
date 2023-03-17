import pytest

from pieces.ntheory.functions import (
    I,
    N,
    DivisorsSumFunction,
    big_omega,
    d,
    little_omega,
    mobius,
    sigma,
    totient,
    totient_inverse,
    u,
)


class TestTotient:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 2),
            (5, 4),
            (6, 2),
            (7, 6),
            (8, 4),
            (9, 6),
            (10, 4),
        ],
    )
    def test_values(self, k, expected):
        assert totient(k) == expected

    def test_repr(self):
        assert repr(totient) == "totient"

    def test_equality(self):
        assert totient**-1 == totient_inverse
        assert totient * (totient**-1) == I


class TestMobius:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 1),
            (2, -1),
            (3, -1),
            (4, 0),
            (5, -1),
            (6, 1),
            (7, -1),
            (8, 0),
            (9, 0),
            (10, 1),
        ],
    )
    def test_values(self, k, expected):
        assert mobius(k) == expected

    def test_repr(self):
        assert repr(mobius) == "mobius"

    def test_equality(self):
        assert mobius**-1 == u
        assert mobius * (mobius**-1) == I


class TestLittleOmega:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 0),
            (2 * 3 * 5, 1 + 1 + 1),
            (2**2 * 3**3 * 5**4, 1 + 1 + 1),
        ],
    )
    def test_values(self, k, expected):
        assert little_omega(k) == expected

    def test_repr(self):
        assert repr(little_omega) == "little_omega"


class TestBigOmega:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 0),
            (2 * 3 * 5, 1 + 1 + 1),
            (2**2 * 3**3 * 5**4, 2 + 3 + 4),
        ],
    )
    def test_values(self, k, expected):
        assert big_omega(k) == expected

    def test_repr(self):
        assert repr(big_omega) == "big_omega"


class TestIdentity:
    def test_values(self):
        assert I(1) == 1
        for k in range(2, 100):
            assert I(k) == 0

    def test_repr(self):
        assert repr(I) == "I"

    def test_inverse(self):
        assert I**-1 == I
        assert I * (I**-1) == I


class TestN:
    @pytest.mark.parametrize("k, expected", [(x, x) for x in range(1, 100)])
    def test_values(self, k, expected):
        assert N(k) == expected

    def test_repr(self):
        assert repr(N) == "N"

    def test_inverse(self):
        assert N * (N**-1) == I


class TestUnit:
    @pytest.mark.parametrize("k, expected", [(x, 1) for x in range(1, 100)])
    def test_values(self, k, expected):
        assert u(k) == expected

    def test_repr(self):
        assert repr(u) == "u"

    def test_inverse(self):
        assert u**-1 == mobius
        assert u * (u**-1) == I


class TestNumberOfDivisors:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 1),
            (2, 2),
            (3, 2),
            (4, 3),
            (5, 2),
            (6, 4),
            (7, 2),
            (8, 4),
            (9, 3),
            (10, 4),
        ],
    )
    def test_values(self, k, expected):
        assert d(k) == expected

    def test_repr(self):
        assert repr(d) == "d"

    def test_inverse(self):
        assert d**-1 == mobius * mobius
        assert d * (d**-1) == I


class TestDivisorsSum:
    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 1),
            (2, 3),
            (3, 4),
            (4, 7),
            (5, 6),
            (6, 12),
            (7, 8),
            (8, 15),
            (9, 13),
            (10, 18),
        ],
    )
    def test_values(self, k, expected):
        assert sigma(k) == expected

    def test_repr(self):
        assert repr(sigma) == "sigma"

    def test_inverse(self):
        assert sigma * (sigma**-1) == I


class TestSquareDivisorSum:
    

    @pytest.mark.parametrize(
        "k,expected",
        [
            (1, 1),
            (2, 5),
            (3, 10),
            (4, 21),
            (5, 26),
            (6, 50),
            (7, 50),
            (8, 85),
            (9, 91),
            (10, 130),
        ],
    )
    def test_values(self, k, expected):
        sigma2 = DivisorsSumFunction(2)
        assert sigma2(k) == expected

    def test_inverse(self):
        sigma2 = DivisorsSumFunction(2)
        assert sigma2 * (sigma2**-1) == I



