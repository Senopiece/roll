from typing import Any
from cyclic import cmul


class G:
    S = 32  # global bit length
    _n: int

    def __init__(self, x: int) -> None:
        self._n = cmul(x, x, self.S)

    @classmethod
    def _raw(cls, n: int):
        obj = cls.__new__(cls)
        obj._n = n
        return obj

    def __mul__(self, other: Any):
        if not isinstance(other, G):
            raise TypeError()
        return G._raw(cmul(self._n, other._n, self.S))

    def __eq__(self, other: Any):
        if not isinstance(other, G):
            raise TypeError()
        return self._n == other._n

    def __repr__(self) -> str:
        return str(self._n)


# This sign approach requires
# - No division operation to be feasible on the cipher (e.g. no Gx / a)
# - A underlying periodicity to be either
#   hard to find and hence unknown or just with no period at all.
#   Or a even period, so that 2 cannot have multiplicative inverse.
#   So that multiplecative inverse cannot be used to simulate division.

# h - message hash (S bits)
# Gk - signer private key (S bits)
# G2k - signer public key (S bits)
# Gs - sign (S bits)


def sign(h: int, Gk: G):
    return G(h) * Gk


G2 = G(2)


def verify(h: int, Gs: G, G2k: G):
    return Gs * G2 == G2k * G(h)


if __name__ == "__main__":
    h = 32423532434

    Gk = G(324325)
    G2k = G2 * Gk
    Gs = sign(h, Gk)

    print(verify(h, Gs, G2k))

# TODO: check vulanabilities
