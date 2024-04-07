from typing import Any
from cyclic import cmul


class G:
    S = 128  # global bit length
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
#   So that multiplecative inverse cannot be used to simulate division

# h - message hash (S/2 bits recommended)
# k - signer private key (S/2 bits recommended)
# Gk - signer public key (S bits)
# Gs - sign (S bits)
# Hovewer can sign only iff k*h < 2^S, so it's better to have S/2 private key and message hash


def sign(h: int, k: int):
    assert k % 2 == 0
    return G(h * k // 2)


G2 = G(2)


def verify(h: int, Gs: G, Gk: G):
    return Gs * G2 == Gk * G(h)


if __name__ == "__main__":
    h = 324235

    k = 235666
    Gk = G(k)

    Gs = sign(567, k)

    print(verify(h, Gs, Gk))

# TODO: check vulanabilities
