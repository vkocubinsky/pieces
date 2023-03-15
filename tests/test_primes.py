from pieces.ntheory.primes import is_prime, pi, primes, sieve

limit = 30
prepared_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_pi():
    for x in range(1, limit + 1):
        assert pi(x) == len(primes(x))


def test_sieve():
    assert sieve(limit) == prepared_primes


def test_primes():
    assert primes(limit) == prepared_primes


def test_is_prime():
    for x in range(1, limit + 1):
        if x in prepared_primes:
            assert is_prime(x)
        else:
            assert not is_prime(x)
