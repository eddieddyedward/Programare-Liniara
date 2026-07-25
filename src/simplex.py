from copy import deepcopy
import numpy as np

from tabel import CalculDelta, PrintareSolutie

np.set_printoptions(suppress=True, precision=6)


def ValidareSolutie(Ziteratii, sol, n_princ, c_initial):

    suma = 0

    for j in range(n_princ):
        suma += sol[j] * c_initial[j]

    if abs(suma - Ziteratii) < 1e-6:
        print("Solutia se valideaza")
    else:
        print("Solutia NU se valideaza")


def VerificareOptimalitate(opt, delta, iteratie):

    if opt == 1:

        if any(d > 0 for d in delta):
            print("Continuam cu urmatoarea iteratie:")
            return False

        print(f"Aceasta este iteratia stop ({iteratie}):")
        return True

    else:

        if any(d < 0 for d in delta):
            print("Continuam cu urmatoarea iteratie:")
            return False

        print(f"Aceasta este iteratia stop ({iteratie}):")
        return True


def UrmatoareaIteratie(iteratie, opt, delta, m, n, T, c):

    print()

    lista = []
    T_UrmatoareaIteratie = deepcopy(T)

    if opt == 1:
        colpiv = delta.index(max(delta)) + 3
    else:
        colpiv = delta.index(min(delta)) + 3

    for i in range(m):

        if T[i][colpiv] > 0:
            lista.append(T[i][2] / T[i][colpiv])
        else:
            lista.append(float("inf"))

    if all(x == float("inf") for x in lista):

        if opt == 1:
            print("Solutia problemei este infinit")
        else:
            print("Solutia problemei este -infinit")

        exit()

    linpiv = lista.index(min(lista))

    P = T[linpiv][colpiv]

    print(f"Vectorul coloana care iese din baza este a{T[linpiv][1]}")
    print(f"Vectorul coloana care intra in baza este a{colpiv-2}")
    print(f"Pivotul este elementul {P} de pe coloana {colpiv} si randul {linpiv}")

    T_UrmatoareaIteratie[linpiv][0] = c[colpiv - 3]
    T_UrmatoareaIteratie[linpiv][1] = colpiv - 2

    for j in range(2, n + 2):
        T_UrmatoareaIteratie[linpiv][j] = T[linpiv][j] / P

    for i in range(m):
        if i != linpiv:
            T_UrmatoareaIteratie[i][colpiv] = 0

    for i in range(m):

        if i == linpiv:
            continue

        for j in range(2, n + 2):

            if j == colpiv:
                continue

            T_UrmatoareaIteratie[i][j] = (
                P * T[i][j] - T[i][colpiv] * T[linpiv][j]
            ) / P

    print(np.array(T_UrmatoareaIteratie))

    return T_UrmatoareaIteratie


def RezolvaSimplex(T, B, c, opt, n, m, n_princ, c_initial):

    iteratie = 1

    while True:

        Ziteratii, delta = CalculDelta(T, n, m, c)

        print(f"Z: {np.array(Ziteratii)}")

        for j in range(n):
            print(f"Delta[{j+1}]: {delta[j]}")

        print()

        if VerificareOptimalitate(opt, delta, iteratie):

            for i in range(m):
                if abs(T[i][0]) == 1000 and T[i][2] != 0:
                    print("Problema nu are solutie")
                    return

            print(f"f({opt}) = {Ziteratii[-1]}")

            sol = PrintareSolutie(T, m, n_princ)

            ValidareSolutie(
                Ziteratii[-1],
                sol,
                n_princ,
                c_initial
            )

            return

        iteratie += 1

        T = UrmatoareaIteratie(
            iteratie,
            opt,
            delta,
            m,
            n,
            T,
            c
        )