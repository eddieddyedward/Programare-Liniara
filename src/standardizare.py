def Standardizare(A, b, c, restrictii, restrictii_speciale, opt):

    m = len(A)
    n = len(c)

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

    return A, b, c, n