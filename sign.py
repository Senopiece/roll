from abc import ABC, abstractmethod
from typing import Any

# Defining
# h - message hash (S bits)
# Ek - signer private key (S bits)
# Epk = Ek*key_mul - signer public key (S bits)
# Es - sign (S bits)

# This sign approach requires
# - A bounded space E where E(x) is easy, but the opposite is not
#   - hence no comparison to be feasible in E
# - A commutative and associative addition by a number to be defined in E
#   > that actually does not really need to work as a addition, but just to be commutative and associative
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


# this thing is just for example - it has well calculable period, but other properties are ok
class E32Exp(E):
    S = 32  # global bit length
    M = pow(S, 2)
    G = 11  # generator point - aka E(0)
    VS = 1  # variation shift - tweaking it makes another group but with the same period
    _n: int

    @classmethod
    def _mul(cls, a: int, b: int):
        return (a * b) % cls.M

    def __init__(self, x: int) -> None:
        self._n = (self.VS * pow(self.G, x, self.M)) % self.M

    @classmethod
    def raw(cls, n: int):
        obj = cls.__new__(cls)
        obj._n = n
        return obj

    def __add__(self, other: Any):
        if not isinstance(other, E32Exp):
            raise TypeError()
        return E32Exp.raw(
            self._mul(
                self._n,
                other._n,
            )
        )

    def __mul__(self, n: int):
        return E32Exp.raw(pow(self._n, n, self.M))

    def __eq__(self, other: Any):
        if not isinstance(other, E32Exp):
            raise TypeError()
        return self._n == other._n

    def __repr__(self) -> str:
        return str(self._n)


KEY_MUL = 2


def f(h: int) -> E32Exp:
    # return E(h) # is not safe since with it attacker has a pretty decent chance
    #               to falsify a sign knowing at least one valid sign
    #               falsification: E(k) + E(h2) = Es1 + E(d) = (E(k) + E(h1)) + E(d), d = h2 - h1
    #                              if h2 > h1 -> E(d) is easy to calculate
    return E32Exp.raw(h)  # this may be out of subgroup - seems to be ok, but is it?


def sign(h: int, Ek: E):
    return Ek + f(h)


def verify(h: int, Es: E, Epk: E):
    # (k + f(h)) * KEY_MUL == k*KEY_MUL + f(h)*KEY_MUL requires commutability and associativity
    return Es * KEY_MUL == Epk + f(h) * KEY_MUL


if __name__ == "__main__":
    h = 324235324349912

    Ek = E32Exp(7794992043)  # private key
    Epk = Ek * KEY_MUL  # public key
    Es = sign(h, Ek)

    print(verify(h, Es, Epk))
