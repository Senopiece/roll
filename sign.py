from cyclic import cmul

S = 128  # bit length


def G(x: int):
    return cmul(x, x, S)


def mulG(x: int, y: int):
    return cmul(x, y, S)


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


def verify(h: int, Gs: int, Gk: int):
    return mulG(Gs, G2) == mulG(Gk, G(h))


if __name__ == "__main__":
    h = 324235

    k = 235666
    Gk = G(k)

    Gs = sign(h, k)

    print(verify(h, Gs, Gk))

# TODO: check vulanabilities
