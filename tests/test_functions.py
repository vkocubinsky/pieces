from math import exp

import pytest

from pieces.ntheory.functions import (
    N,
    big_omega,
    identity,
    little_omega,
    mobius,
    sigma,
    tau,
    totient,
    totient_inverse,
    unit,
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

    def test_formula(self):
        assert totient.formula == "φ"

    def test_equality(self):
        assert totient**-1 == totient_inverse
        assert totient * totient_inverse == identity


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

    def test_formula(self):
        assert mobius.formula == "μ"

    def test_equality(self):
        assert mobius**-1 == unit
        assert mobius * unit == identity


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

    def test_formula(self):
        assert little_omega.formula == "ω"


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

    def test_formula(self):
        assert big_omega.formula == "Ω"


class TestIdentity:
    def test_values(self):
        assert identity(1) == 1
        for k in range(2, 100):
            assert identity(k) == 0

    def test_formula(self):
        assert identity.formula == "I"

    def test_inverse(self):
        assert identity**-1 == identity
        assert identity * identity == identity


class TestN:
    @pytest.mark.parametrize("k, expected", [(x, x) for x in range(1, 100)])
    def test_values(self, k, expected):
        assert N(k) == expected

    def test_formula(self):
        assert N.formula == "N"

    def test_inverse(self):
        assert N * (N**-1) == identity


class TestUnit:
    @pytest.mark.parametrize("k, expected", [(x, 1) for x in range(1, 100)])
    def test_values(self, k, expected):
        assert unit(k) == expected

    def test_formula(self):
        assert unit.formula == "u"

    def test_inverse(self):
        assert unit**-1 == mobius
        assert unit * mobius == identity


class TestTau:
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
    # tau = u * u
    def test_values(self, k, expected):
        assert tau(k) == expected

    def test_formula(self):
        assert tau.formula == 'τ'

