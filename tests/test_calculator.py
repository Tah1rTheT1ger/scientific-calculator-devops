import math
import pytest
from calculator import sqrt, factorial, ln, power, DomainError

def test_sqrt_ok():
    assert sqrt(9) == 3
    assert math.isclose(sqrt(2), math.sqrt(2))

def test_sqrt_neg():
    with pytest.raises(DomainError):
        sqrt(-1)

def test_factorial_ok():
    assert factorial(0) == 1
    assert factorial(5) == 120

def test_factorial_bad():
    with pytest.raises(DomainError):
        factorial(-1)
    with pytest.raises(DomainError):
        factorial(3.5)  # type: ignore[arg-type]

def test_ln_ok():
    assert math.isclose(ln(math.e), 1.0, rel_tol=1e-12)

def test_ln_bad():
    with pytest.raises(DomainError):
        ln(0)
    with pytest.raises(DomainError):
        ln(-3)

def test_power_ok():
    assert power(2, 10) == 1024
    assert power(-2, 2) == 4

def test_power_bad():
    with pytest.raises(DomainError):
        power(-2, 0.5)
