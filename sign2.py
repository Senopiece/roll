# refer to sign.py for the idea

from typing import Any
from cyclic import cmul


# TODO: find approaches to hack it
class CSqr:
    S = 32  # global bit length
    _n: int

    @classmethod
    def _mul(cls, a: int, b: int):
        return cmul(a, b, cls.S)

    def __init__(self, x: int) -> None:
        self._n = self._mul(x, x)

    @classmethod
    def raw(cls, n: int):
        obj = cls.__new__(cls)
        obj._n = n
        return obj

    def __mul__(self, other: Any):
        if not isinstance(other, CSqr):
            raise TypeError()
        return CSqr.raw(
            self._mul(
                self._n,
                other._n,
            )
        )

    def __eq__(self, other: Any):
        if not isinstance(other, CSqr):
            raise TypeError()
        return self._n == other._n

    def __repr__(self) -> str:
        return str(self._n)


KEY_MUL = CSqr.raw(2)


def f(h: int) -> CSqr:
    return CSqr.raw(h)  # this may be out of subgroup - seems to be ok, but is it?
    # return CSqr(h)  # here this impl is also safe by two reasons:
    #                   1. it's really unlikely for two hashes to be devisable
    #                   2. even if the're devisable CSqr is so weird that E(h1)*E(h2/h1) != E(h2)
    #                   * so the second is stronger that the first,
    #                     but i need to mention the first to remind you
    #                     (in case you've probing another E that has no second property
    #                      - dont forget that it's still strong enough due to the first point)
    # but CSqr.raw(h) is chosen because it's faster


def sign(h: int, Ek: CSqr):
    return Ek * f(h)


def verify(h: int, Es: CSqr, Epk: CSqr):
    # works because (k * f(h)) * KEY_MUL == (k * KEY_MUL) * f(h)
    # TODO: investigate why it has some weird math since:
    #    (k * f(h)) * KEY_MUL != f(h) * (k * KEY_MUL)
    #    (f(h) * k) * KEY_MUL != (k * KEY_MUL) * f(h)
    return Es * KEY_MUL == Epk * f(h)


if __name__ == "__main__":
    h = 1123568764323

    Ek = CSqr(25823245)  # private key
    Epk = Ek * KEY_MUL  # public key
    Es = sign(h, Ek)

    print(verify(h, Es, Epk))
