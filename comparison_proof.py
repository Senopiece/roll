# proof that Ea > Eb

# this thing can be used for example in blockchain with hidden balances:
#  https://github.com/Senopiece/balance_cipher/blob/main/balance_cipher.py


from sign import FibMat

# requires E like from sign.py
# without E like from sign.py the proof would look like
#  https://github.com/Senopiece/balance_cipher/blob/main/comparison_proofs.py


def proof(a: int, b: int):
    # proof can be made only if one knows both raw values
    assert a > b
    return FibMat(a - b)


def verify(Ep: FibMat, Ea: FibMat, Eb: FibMat):
    # relying on the fact that finding a proof is unfeasible if a < b
    return Ea == Eb + Ep


if __name__ == "__main__":
    a = 3457834959399
    b = 345995

    Ep = proof(a, b)
    Ea = FibMat(a)
    Eb = FibMat(b)

    print(verify(Ep, Ea, Eb))
