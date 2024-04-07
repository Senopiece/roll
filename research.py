from typing import List

from cyclic import cadd, cmul


def add(a: int, b: int):
    return (a + b) % M


def mul(a: int, b: int):
    return (a * b) % M


# best period: M (if P is not 0)
def P_add_a(a: int):
    return add(P, a)


# best period: M (if P is not 0)
def c_P_add_a(a: int):
    return cadd(P, a, S)


# best period: M (if P is mutual prime to M and is not 0)
def P_mul_a(a: int):
    return mul(P, a)


# best period: M^2 (if P is not 0 - ya just not a 0 wow!)
def c_P_mul_a(a: int):
    return cmul(P, a, S)


# NOTE: it gives very symmetric image, but when selecting each M'th row, the image is very random
# best so far found period: M/2 ~ M
def a_mul_a(a: int):
    return mul(a, a)


# best so far found period: M(M-1) ~ M^2
def c_a_mul_a(a: int):
    return cmul(a, a, S)


# best so far found period: M
def a_to_P(a: int):
    # returns a^P
    res = 1
    for bit in bin(P)[2:]:
        res = mul(res, res)
        if bit == "1":
            res = mul(res, a)
    return res


# best so far found period: M
def c_a_to_P(a: int):
    # returns a^P
    res = 1
    for bit in bin(P)[2:]:
        res = cmul(res, res)
        if bit == "1":
            res = cmul(res, a)
    return res


# best so far found period: 0.25M ~ M
def P_to_a(a: int):
    # returns P^a
    res = 1
    for bit in bin(a)[2:]:
        res = mul(res, res)
        if bit == "1":
            res = mul(res, P)
    return res


# TODO: find ways to solve such discrete log
# TODO: find a way to calculate the period for this function without full enumeration (recall how it's done in a regular case with euler's theorem)
# best so far found period: 0.9M ~ M
def c_P_to_a(a: int):
    # returns cyclic P^a
    res = 1
    for bit in bin(a)[2:]:
        res = cmul(res, res, S)
        if bit == "1":
            res = cmul(res, P, S)
    return res


# best so far found period: M, but on S > 6 didnt find yet
def a_to_a(a: int):
    # returns a^a
    res = 1
    for bit in bin(a)[2:]:
        res = mul(res, res)
        if bit == "1":
            res = mul(res, a)
    return res


# best so far found period: M(M/2-1) ~ M^2
def c_a_to_a(a: int):
    # returns cyclic a^a
    res = 1
    for bit in bin(a)[2:]:
        res = cmul(res, res, S)
        if bit == "1":
            res = cmul(res, a, S)
    return res


# just visualize
# S = 5
M = 2 * 3 * 5
a = ["-"] * M
P = 2
for c in range(M):
    v = P_mul_a(c)
    a = ["-"] * M
    a[v] = "x"
    print(" ".join(a), "<" if c % M == 0 else "", v)

# >>>>

# search for the best period when P is also iterable
# best = (-1, -1, -1)
# shift = 3
# for S in range(5, 8):
#     M = 2**S
#     for P in range(1, M):
#         print(f"Searching period for (S, P) = ({S}, {P})...")

#         values: List[int] = []
#         found = False
#         for c in range(
#             shift, M**M + 4 + shift
#         ):  # assuming no greater than this value period can be found
#             v = c_P_mul_a(c)
#             values.append(v)
#             p = len(values) // 2
#             if len(values) % 2 == 0 and values[:p] == values[p:]:
#                 print(p, "that is", f"{p/M}*M,", f"M = {M}")
#                 if p > best[2]:
#                     best = S, P, p
#                 found = True
#                 break

#         if not found:
#             print("No period found")

# if best[0] != -1:
#     S, P, p = best
#     M = 2**S
#     print(
#         f"Best found: (S, P) = ({S}, {P}) with period = {p}",
#         "that is",
#         f"{p/M}*M,",
#         f"M = {M}",
#     )

# >>>>

# search for the best period when P is not iterable
# P = 3
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
