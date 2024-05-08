# long arithmetic matrices

from typing import List

Mat = List[List[int]]


def matrix_mod_mul(a: Mat, b: Mat, m: int) -> Mat:
    """
    Multiply two matrices a and b under modulo m.
    """
    rows = len(a)
    cols = len(b[0])
    result = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            for k in range(len(b)):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % m

    return result


def identity(n: int) -> Mat:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def fast_matrix_pow(matrix: Mat, n: int, m: int) -> Mat:
    """
    Raise a matrix to the power n modulo m using an iterative method.
    """
    result = identity(len(matrix))
    base = matrix

    while n > 0:
        if n % 2 == 1:
            result = matrix_mod_mul(result, base, m)
        base = matrix_mod_mul(base, base, m)
        n //= 2

    return result


if __name__ == "__main__":
    # Example usage
    A = [[0, 1], [1, 1]]
    print(fast_matrix_pow(A, 100, 100000))
