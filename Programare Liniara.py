import numpy as np
from copy import deepcopy
import math

n_princ = 0

def ValidareSolutie(Ziteratii, sol):

    suma = 0
    for j in range(n_princ):
        suma = suma + sol[j]*c_initial[j]
    if suma == Ziteratii:
        print("Solutia se valideaza")
    else:
        print("Solutia NU se valideaza")

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
            lista.append(float('inf'))

    if all(x == float('inf') for x in lista):
        if opt == 1:
            print("Solutia problemei este infinit")
        else:
            print("Solutia problemei este -infinit")
        exit()

    linpiv = lista.index(min(lista))

    P = T[linpiv][colpiv]

    print(f"Vectorul coloana care iese din baza este a{T[linpiv][1]}")
    print(f"Vectorul coloana care intra in baza este a{colpiv - 2}")
    print(f"Pivotul este elementul {P} de pe coloana {colpiv} si randul {linpiv}")

    T_UrmatoareaIteratie[linpiv][0] = c[colpiv - 3]
    T_UrmatoareaIteratie[linpiv][1] = colpiv - 2
    for j in range(2, n + 2):
        T_UrmatoareaIteratie[linpiv][j] = T[linpiv][j] / P
    for i in range(m):
        if i != linpiv:
            T_UrmatoareaIteratie[i][colpiv] = 0
    for i in range(m):
        if i == linpiv: continue
        for j in range(2, n + 2):
            if j == colpiv: continue
            T_UrmatoareaIteratie[i][j] = (P * T[i][j] - T[i][colpiv] * T[linpiv][j]) / P

    print(np.array(T_UrmatoareaIteratie))
    return T_UrmatoareaIteratie


def PrintareSolutie(T, m, B):

    sol = [0] * n_princ
    for i in range(m):
        for j in range(n_princ):
            if T[i][1] == j + 1:
                sol[j] = T[i][2]
    print(f"x0: {np.array(sol)}")
    return sol


def VerificareOptimalitate(opt, delta, iteratie, T, n, m):

    if opt == 1:
        if any(d > 0 for d in delta):
            print("Continuam cu urmatoarea iteratie: ")
            return False
        else:
            print(f"Aceasta este iteratia stop ({iteratie}) : ")
            return True
    else:
        if any(d < 0 for d in delta):
            print("Continuam cu urmatoarea iteratie: ")
            return False
        else:
            print(f"Aceasta este iteratia stop ({iteratie}) : ")
            return True

def CalculDelta(T, n, m, c):

    Ziteratii = []
    suma = 0
    z = [0] * n
    delta = []

    for i in range(m):
        suma = suma + (T[i][0] * T[i][2])
    Ziteratii.append(suma)

    for j in range(n):
        for i in range(m):
            z[j] += T[i][0] * T[i][j + 3]

    for j in range(n):
        delta.append(c[j] - z[j])

    z = list(map(int, z))
    delta = list(map(int, delta))

    return Ziteratii, delta


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
    print("Introduceti inegalitatile din restrictiile speciale(>= - 1; <= - 2; apartine lui R - 3):")
    for i in range(n):
        restrictii_speciale[i] = int(input(f"restrictii_speciale[{i}] = "))


    global n_princ
    global c_initial
    n_princ = n
    c_initial = c

    # REGULI DE STANDARDIZARE
    # R1 - se aplica pentru restrictiile speciale

    j = 0
    while j < n:
        if restrictii_speciale[j] == 2:
            for i in range(m):
                A[i][j] *= -1
            c[j] *= -1
            restrictii_speciale[j] = 1
        elif restrictii_speciale[j] == 3:
            for i in range(m):
                A[i].insert(j + 1, -A[i][j])
            c.insert(j + 1, -c[j])
            restrictii_speciale.insert(j + 1, 1)
            restrictii_speciale[j] = 1
            j += 1
            n += 1
        j += 1

    # R2 - se aplica pentru restrictii

    y = []
    z = []
    cy = []
    cz = []

    for i in range(m):
        if restrictii[i] == 1:
            coly = [0] * m
            coly[i] = 1
            y.append(coly)
            cy.append(0)
            restrictii_speciale.append(1)
        elif restrictii[i] == 2:
            colz = [0] * m
            colz[i] = 1
            z.append(colz)
            if opt == 0:
                cz.append(1000)
            else:
                cz.append(-1000)
            restrictii_speciale.append(1)
        else:
            coly = [0] * m
            coly[i] = -1
            y.append(coly)
            cy.append(0)
            restrictii_speciale.append(1)
            colz = [0] * m
            colz[i] = 1
            z.append(colz)
            if opt == 0:
                cz.append(1000)
            else:
                cz.append(-1000)
            restrictii_speciale.append(1)

    for col in y:
        for i in range(m):
            A[i].append(col[i])

    for col in z:
        for i in range(m):
            A[i].append(col[i])

    c.extend(cy)
    c.extend(cz)
    n = len(c)


    iteratie = 1
    T, B = TabelSimplex(n, m, A, b, c)
    print(f"Tabelul simplex pentru iteratia {iteratie-1}: ")
    print(np.array(T))
    print()

    while True:
        Ziteratii, delta = CalculDelta(T, n, m, c)
        print(f"Z: {np.array(Ziteratii)}")
        for j in range(n):
            print(f"Delta[{j + 1}]: {delta[j]}")
        print()
        if VerificareOptimalitate(opt, delta, iteratie,T, n, m) == True:
            for i in range(m):
                if abs(T[i][0]) == 1000 and T[i][2] != 0:
                    print("Problema nu are solutie")
                    return
            print(f"f({opt}) = {Ziteratii[-1]}")
            sol = PrintareSolutie(T, m, B)
            ValidareSolutie(Ziteratii[-1], sol)
            return
        else:
            iteratie += 1
            T = UrmatoareaIteratie(iteratie, opt, delta, m, n, T, c)


Meniu()