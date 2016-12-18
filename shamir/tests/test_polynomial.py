from shamir import Polynomial


def test_polynomial():
    coefficients = [5, 1, 2, 33, 4]
    polynomial = Polynomial(coefficients)
    assert polynomial(0) == coefficients[0]
    assert polynomial(1) == sum(coefficients)
