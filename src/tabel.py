import numpy as np

np.set_printoptions(suppress=True, precision=6)


def TabelSimplex(n, m, A, b, c):

    T = []
    A = np.array(A)
    m, n = A.shape
    B = [0] * m
    cB = []

    for j in range(n):
        col = A[:, j]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            linie = np.where(col == 1)[0][0]
            B[linie] = j + 1

    for i in range(m):
        for j in range(n):
            if B[i] - 1 == j:
                cB.append(c[j])

    for i in range(m):
        T.append([b[i]])

    for i in range(m):
        T[i].extend(A[i])

    for i in range(m):
        T[i].insert(0, B[i])

    for i in range(m):
        T[i].insert(0, cB[i])

    return T, B


def CalculDelta(T, n, m, c):

    Ziteratii = []
    suma = 0
    z = [0] * n
    delta = []

    for i in range(m):
        suma += T[i][0] * T[i][2]

    Ziteratii.append(suma)

    for j in range(n):
        for i in range(m):
            z[j] += T[i][0] * T[i][j + 3]

    for j in range(n):
        delta.append(c[j] - z[j])

    z = [round(x, 6) for x in z]
    delta = [round(x, 6) for x in delta]

    return Ziteratii, delta


def PrintareSolutie(T, m, n_princ):

    sol = [0] * n_princ

    for i in range(m):
        for j in range(n_princ):
            if T[i][1] == j + 1:
                sol[j] = T[i][2]

    sol = [round(x, 6) for x in sol]

    print(f"x0: {np.array(sol)}")

    return sol