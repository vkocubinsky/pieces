from pieces.ntheory.factorization import defactorize, factorize, pvaluation


def test_pvaluation():
    assert pvaluation(2**3 * 35, 2) == 3


def test_defactorize_factorize():
    for k in range(1, 100):
        assert defactorize(factorize(k)) == k
