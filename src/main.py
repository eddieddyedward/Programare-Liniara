import numpy as np

from standardizare import Standardizare
from tabel import TabelSimplex
from simplex import RezolvaSimplex

np.set_printoptions(suppress=True, precision=6)


def Meniu():

    print("------------------------------PROGRAMARE LINIARA------------------------------")
    print()

    opt = int(input("Optimul functiei este max sau min? (max - 1; min - 0): "))

    n = int(input("Introduceti numarul de variabile: "))
    m = int(input("Introduceti numarul de restrictii: "))

    A = [[0 for _ in range(n)] for _ in range(m)]

    print("Introduceti matricea A:")
    for i in range(m):
        for j in range(n):
            A[i][j] = int(input(f"A[{i}][{j}]: "))

    b = [0 for _ in range(m)]

    print("Introduceti vectorul coloana b:")
    for i in range(m):
        b[i] = int(input(f"b[{i}]: "))

    c = [0 for _ in range(n)]

    print("Introduceti coeficientii functiei obiectiv c:")
    for i in range(n):
        c[i] = int(input(f"c[{i}] = "))

    restrictii = [0 for _ in range(m)]

    print("Introduceti egalitatile sau inegalitatile din restrictii (<= - 1; = - 2; >= - 3):")
    for i in range(m):
        restrictii[i] = int(input(f"restrictii[{i}] = "))

    restrictii_speciale = [0 for _ in range(n)]

    print("Introduceti inegalitatile din restrictiile speciale (>= - 1; <= - 2; apartine lui R - 3):")
    for i in range(n):
        restrictii_speciale[i] = int(input(f"restrictii_speciale[{i}] = "))

    # salvam numarul initial de variabile si coeficientii functiei obiectiv
    n_princ = n
    c_initial = c.copy()

    # standardizarea problemei
    A, b, c, n = Standardizare(
        A,
        b,
        c,
        restrictii,
        restrictii_speciale,
        opt
    )

    # construirea tabelului simplex
    T, B = TabelSimplex(n, m, A, b, c)

    print("Tabelul simplex pentru iteratia 0:")
    print(np.array(T))
    print()

    # rezolvarea problemei
    RezolvaSimplex(
        T,
        B,
        c,
        opt,
        n,
        m,
        n_princ,
        c_initial
    )


if __name__ == "__main__":
    Meniu()