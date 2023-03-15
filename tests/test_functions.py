import pytest

from pieces.ntheory.functions import (
    big_omega,
    identity,
    little_omega,
    mobius,
    totient,
    totient_inverse,
    unit,
)

# TODO:
# sigma0 == tau
# test multiplicativity?

class TestTotient:
    @pytest.mark.parametrize(
        "k,expected_value",
        [(1, 1), (2, 1), (3, 2), (4, 2), (5, 4), (6, 2), (7, 6), (8, 4), (9, 6), (10, 4)],
    )
    def test_totient_values(self, k, expected_value):
        assert totient(k) == expected_value


    def test_totient_formula(self):
        assert totient.formula == "φ"


    def test_totient_equality(self):
        assert (~totient) == totient_inverse
        assert (~totient).formula == "φ⁻¹"
        assert totient * totient_inverse == identity


class TestMobius: 
    @pytest.mark.parametrize(
        "k,expected_value",
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
    def test_mobius_values(self, k, expected_value):
        assert mobius(k) == expected_value


    def test_mobius_formula(self):
        assert mobius.formula == "μ"


    def test_mobius_equality(self):
        assert (~mobius) == unit
        assert (~mobius).formula == "u"
        assert mobius * unit == identity


class TestLittleOmega:
    @pytest.mark.parametrize(
        "k,expected_value",
        [
            (1, 0),
            (2 * 3 * 5, 1 + 1 + 1),
            (2**2 * 3**3 * 5**4, 1 + 1 + 1),
        ],
    )
    def test_little_omega(self, k, expected_value):
        assert little_omega(k) == expected_value


    def test_little_omega_formula(self):
        assert little_omega.formula == "ω"


class TestBigOmega:

    @pytest.mark.parametrize(
        "k,expected_value",
        [
            (1, 0),
            (2 * 3 * 5, 1 + 1 + 1),
            (2**2 * 3**3 * 5**4, 2 + 3 + 4),
        ],
    )
    def test_big_omega(self,k, expected_value):
        assert big_omega(k) == expected_value


    def test_big_omega_formula(self):
        assert big_omega.formula == "Ω"

class TestIdentity:
    def test_identity(self):
        assert identity(1) == 1
        for k in range(2, 100):
            assert identity(k) == 0


    def test_identity_formula(self):
        assert identity.formula == "I"

    def test_identity_inverse(self):
        assert identity * identity == identity 
        assert ~identity == identity



