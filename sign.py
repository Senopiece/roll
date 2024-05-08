from abc import ABC, abstractmethod
from typing import Any

from matrix import Mat, fast_matrix_pow, matrix_mod_mul

# Defining
# h - message hash (S bits)
# Ek - signer private key (S bits)
# Epk = Ek*key_mul - signer public key (S bits)
# Es - sign (S bits)

# This sign approach requires
# - A bounded space E where E(x) is easy, but the opposite is not
#   - hence no comparison to be feasible in E
# - (a + b) * c = a*c + b*c to hold true in E
# - No subtraction and division to be feasible in E
# - No negative and inverse elements to be feasible in E
#   > A underlying periodicity to be either
#     hard to find and hence unknown or just with no period at all.
# - (optionally) key_mul*x to produce well span over the space
#   > for regular multiplication by modulo this means that key_mul is mutual prime to the hidden modulo
#     so that maybe it can be proven without knowing the actual period


class E(ABC):
    @abstractmethod
    def __add__(self, other: Any) -> "E":
        raise NotImplementedError()

    @abstractmethod
    def __mul__(self, other: int) -> "E":
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError()


# computing the periodicity of this group is known as pisano period
# for a prime M the fastest known way to compute it is O(M)
# so it's suitable because it's underlying periodicity is hard to find and hence unknown
class FibMat(E):
    S = 127  # global bit length
    M = pow(S, 2) - 1
    _data: Mat

    def __init__(self, x: int) -> None:
        F1: Mat = [[0, 1], [1, 1]]
        self._data = fast_matrix_pow(F1, x, self.M)

    @classmethod
    def raw(cls, data: Mat):
        obj = cls.__new__(cls)
        obj._data = data
        return obj

    def __add__(self, other: Any):
        if not isinstance(other, FibMat):
            raise TypeError()
        return FibMat.raw(
            matrix_mod_mul(
                self._data,
                other._data,
                self.M,
            )
        )

    def __mul__(self, n: int):
        return FibMat.raw(fast_matrix_pow(self._data, n, self.M))

    def __eq__(self, other: Any):
        if not isinstance(other, FibMat):
            raise TypeError()
        return self._data == other._data

    def __repr__(self) -> str:
        return str(self._data)


KEY_MUL = 2


def f(h: int) -> FibMat:
    # return E(h) # is not safe since with it attacker has a pretty decent chance
    #               to falsify a sign knowing at least one valid sign
    #               falsification: E(k) + E(h2) = Es1 + E(d) = (E(k) + E(h1)) + E(d), d = h2 - h1
    #                              if h2 > h1 -> E(d) is easy to calculate

    # TODO: research mb not stick to fib and allow to set hash to raw data
    #       that is out of the subgroup, but seems to be ok with it,
    #       moreover it also seems that even known pisano period will not help to hack if hash is used in raw
    # return FibMat.raw([[hash(h+1) % FibMat.M, h], [h, hash(h+2) % FibMat.M]])

    return FibMat(h) * h  # looks to be ok, but maybe there is a better way


def sign(h: int, Ek: E):
    return Ek + f(h)


def verify(h: int, Es: E, Epk: E):
    # (k + f(h)) * KEY_MUL == k*KEY_MUL + f(h)*KEY_MUL
    return Es * KEY_MUL == Epk + f(h) * KEY_MUL


if __name__ == "__main__":
    h = 324235324349912

    Ek = FibMat(7794992043)  # private key
    Epk = Ek * KEY_MUL  # public key
    Es = sign(h, Ek)

    print(verify(h, Es, Epk))
