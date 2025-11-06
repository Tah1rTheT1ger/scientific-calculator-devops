import math

class DomainError(ValueError):
    pass

def sqrt(x: float) -> float:
    if x < 0:
        raise DomainError("sqrt domain error: x must be >= 0")
    return math.sqrt(x)

def factorial(n: int) -> int:
    if isinstance(n, bool):  # bool is int subclass
        n = int(n)
    if not isinstance(n, int):
        raise DomainError("factorial requires an integer")
    if n < 0:
        raise DomainError("factorial domain error: n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def ln(x: float) -> float:
    if x <= 0:
        raise DomainError("ln domain error: x must be > 0")
    return math.log(x)

def power(a: float, b: float) -> float:
    # Reject negative base with non-integer exponent (would be complex)
    if a < 0 and not float(b).is_integer():
        raise DomainError("power domain error: negative base with non-integer exponent")
    return a ** b

# djkbaSDKLJFBASIDP[OIASDD]