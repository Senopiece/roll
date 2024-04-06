from typing import List


def add(a: int, b: int):
    return (a + b) % M


def cadd(a: int, b: int):
    """
    Perform addition with end-around carry on two integers within a fixed bit length.
    """
    bit_length = S
    modulus = 1 << bit_length

    # trim to ensure a and b are fittable in modulus
    # a %= modulus aka assert a < modulus
    # b %= modulus aka assert b < modulus

    raw = a + b
    carry = (
        raw >> bit_length
    )  # because of a and b are trimmed, we can be sure that carry can be only 0/1
    return (raw + carry) % modulus


def cmul(a: int, b: int):
    res = 0
    for bit in bin(a)[2:]:
        res = cadd(res, res)
        if bit == "1":
            res = cadd(res, b)
    return res


def mul(a: int, b: int):
    return (a * b) % M


# best period: M (if P is not 0)
def P_add_a(a: int):
    return add(P, a)


# best period: M (if P is not 0)
def c_P_add_a(a: int):
    return cadd(P, a)


# best period: M (if P is mutual prime to M and is not 0)
def P_mul_a(a: int):
    return mul(P, a)


# best period: M (if P is not 0 - ya just not a 0 wow!)
def c_P_mul_a(a: int):
    return cmul(P, a)


# best so far found period: M/2
def a_mul_a(a: int):
    return mul(a, a)


# best so far found period: M(M-1) ~ M^2 wow!
def c_a_mul_a(a: int):
    return cmul(a, a)


# best so far found period: 0.25M
def P_to_a(a: int):
    # returns P^a
    res = 1
    for bit in bin(a)[2:]:
        res = mul(res, res)
        if bit == "1":
            res = mul(res, P)
    return res


# best so far found period: 0.9M
def c_P_to_a(a: int):
    # returns cyclic P^a
    res = 1
    for bit in bin(a)[2:]:
        res = cmul(res, res)
        if bit == "1":
            res = cmul(res, P)
    return res


# best so far found period: M
def a_to_a(a: int):
    # returns a^a
    res = 1
    for bit in bin(a)[2:]:
        res = mul(res, res)
        if bit == "1":
            res = mul(res, a)
    return res


# best so far found period: 63M ~ M*(M/2)
def c_a_to_a(a: int):
    # returns cyclic a^a
    res = 1
    for bit in bin(a)[2:]:
        res = cmul(res, res)
        if bit == "1":
            res = cmul(res, a)
    return res


# just visualize
# S = 5
# M = 2**S
# a = ["-"] * M
# P = 3
# for c in range(2 * M):
#     v = a_to_a(c)
#     a = ["-"] * M
#     a[v] = "x"
#     print(" ".join(a), "<" if c % M == 0 else "", v)

# search for the best period when P is also iterable
best = (-1, -1, -1)
shift = 10
for S in range(3, 10):
    M = 2**S
    for P in range(1, M):
        print(f"Searching period for (S, P) = ({S}, {P})...")

        values: List[int] = []
        found = False
        for c in range(
            shift, M * M * M * 2 + shift
        ):  # assuming no greater than M^3 period can be found
            v = c_a_to_a(c)
            values.append(v)
            if (
                len(values) % 2 == 0
                and values[: len(values) // 2] == values[len(values) // 2 :]
            ):
                p = len(values) // 2
                print(p, "that is", f"{p/M}*M,", f"M = {M}")
                if p > best[2]:
                    best = S, P, p
                found = True
                break

        if not found:
            print("No period found")

if best[0] != -1:
    S, P, p = best
    M = 2**S
    print(
        f"Best found: (S, P) = ({S}, {P}) with period = {p}",
        "that is",
        f"{p/M}*M,",
        f"M = {M}",
    )

# search for the best period when is not iterable
# best = (-1, -1)
# for S in range(4, 10):
#     M = 2**S
#     print(f"Searching period for S = {S}...")

#     values: List[int] = []
#     found = False
#     for c in range(M * M * M * 2):  # assuming no greater than M^3 period can be found
#         v = c_P_to_a(c)
#         values.append(v)
#         if (
#             len(values) % 2 == 0
#             and values[: len(values) // 2] == values[len(values) // 2 :]
#         ):
#             p = len(values) // 2
#             print(
#                 p,
#                 "that is",
#                 f"{p/M}*M,",
#                 f"M = {M}",
#             )
#             if p > best[1]:
#                 best = S, p
#             found = True
#             break

#     if not found:
#         print("No period")

# if best[0] != -1:
#     S, p = best
#     M = 2**S
#     print(
#         f"Best found: S = {S} with period = {p}",
#         "that is",
#         f"{p/M}*M,",
#         f"M = {M}",
#     )
