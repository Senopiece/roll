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


# NOTE: does not work
# TODO: it it even possible to make it work, mb not using the regular number approach
def cdiv(a: int, b: int, bit_length: int = 5):
    assert b != 0

    res = [False]
    s = 0
    for bit in bin(a)[2:]:
        s = cadd(s, s, bit_length)
        s = cadd(s, 1, bit_length) if bit == "1" else s

        if s >= b:
            s = csub(s, b, bit_length)
            res.append(True)
        else:
            res.append(False)

    return int("".join("1" if e else "0" for e in res), base=2), s


# NOTE: a refereence implementation on regular numbers
# def div(a: int, b: int, bit_length: int = 5):
#     assert b != 0

#     res = [False]
#     s = 0
#     for bit in bin(a)[2:]:
#         s *= 2
#         s += 1 if bit == "1" else 0

#         if s >= b:
#             s -= b
#             res.append(True)
#         else:
#             res.append(False)

#     return int("".join("1" if e else "0" for e in res), base=2), s
