def cadd(a: int, b: int, bit_length: int = 5):
    """
    Perform addition with end-around carry on two integers within a fixed bit length.
    """
    modulus = 1 << bit_length

    # trim to ensure a and b are fittable in modulus
    a %= modulus
    b %= modulus

    raw = a + b
    carry = (
        raw >> bit_length
    )  # because of a and b are trimmed, we can be sure that carry can be only 0/1
    return (raw + carry) % modulus


# NOTE: this thing is not proven to work, but seems to work
def csub(a: int, b: int, bit_length: int = 5):
    modulus = 1 << bit_length
    return cadd(a, modulus - b - 1, bit_length)


def cmul(a: int, b: int, bit_length: int = 5):
    res = 0
    for bit in bin(a)[2:]:
        res = cadd(res, res, bit_length)
        if bit == "1":
            res = cadd(res, b, bit_length)
    return res


def cdiv(a: int, b: int, bit_length: int = 5):
    period = (1 << bit_length) - 1
    return cmul(a, pow(b, -1, period))
