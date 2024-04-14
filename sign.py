from abc import ABC, abstractmethod
from typing import Any

# Defining
# h - message hash (S bits) - is divisible by hash_multiple
# Ek - signer private key (S bits)
# Epk = E*key_multiplier*k - signer public key (S bits)
# Es - sign (S bits)

# This sign approach requires
# - A bounded space E where E(x) is easy, but the opposite is not
#   - hence no comparison to be feasible in E
# - A commutative and associative multiplication by a number to be defined in E
#   > that actually does not really need to work as a multiplication, but just to be commutative and associative
#   > there is a f(x, y) such that E(f(x, y)) = E(x)*y, but this f is not necessarily x*y - it can be x+y or any other
# - No division to be feasible in E
# - No inverse elements to be feasible in E, or at least protect hash and key_multiplier from inversion
#   > A underlying periodicity to be either
#     hard to find and hence unknown or just with no period at all.
#   > Or, if in E(f(x, y)) = E(x)*y, f(x, y) = x*y (mod m), m must be a multiple of key_multiplier and hash_multiple.
# - Hash must not be divisible by key_multiplier


class E(ABC):
    @abstractmethod
    def __mul__(self, other: int) -> "E":
        # needs to be commutative and associative
        # and to disallow either any inverse or
        # ensure no inverse just for some categories (e.g. no inverse for hash and key_multiplier)
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError()


class E32CSqr(E):
    S = 32  # global bit length
    M = pow(S, 2)
    # period is M // 2
    _n: int

    @classmethod
    def _mul(cls, a: int, b: int):
        return (a * b) % cls.M

    def __init__(self, x: int) -> None:
        self._n = self._mul(x, x)

    @classmethod
    def _raw(cls, n: int):
        obj = cls.__new__(cls)
        obj._n = n
        return obj

    def __mul__(self, other: int):
        # Although with this implementation multiplication directly in E is defined,
        # but the most general interface allows support systems where it is not defined
        #   > e.g. discrete exponentiation has only defined addition in E,
        #     so that only multiplication by a raw number can be feasible
        # so that we can adopt to the most general interface
        # by just moving the raw number to E before multiplication
        return E32CSqr._raw(
            # perform mul in E
            self._mul(
                self._n,
                self._mul(other, other),  # mv raw number to E
            )
        )

    def __eq__(self, other: Any):
        if not isinstance(other, E32CSqr):
            raise TypeError()
        return self._n == other._n

    def __repr__(self) -> str:
        return str(self._n)


def normalized_hash(h: int):
    # make hash not divisible by four but divisible by two
    # so that hash remains uninvertable still not devisable by key_multiplier
    # reminder - correction
    # 0        - +2
    # 1        - +1
    # 2        - 0
    # 3        - -1
    reminder = h % 4
    correction = 2 - reminder
    return h + correction


def sign(h: int, Ek: E):
    h = normalized_hash(h)
    return Ek * h


def verify(h: int, Es: E, Epk: E):
    h = normalized_hash(h)
    # (Ek * h) * 4 == (Ek * 4) * h requires commutability and associativity
    return Es * 4 == Epk * h


if __name__ == "__main__":
    h = 32423532434

    Ek = E32CSqr(324325)
    # assert period of E32CSqr is a power of 2 - true
    # here we use key_multiplier = 4
    Epk = Ek * 4
    Es = sign(h, Ek)

    print(verify(h, Es, Epk))
