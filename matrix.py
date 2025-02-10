import random

def generate_system(n):
    A  = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    x_known = [i + 1 for i in range(n)]
    b = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += A[i][j] * x_known[j]
        b.append(s)
    return A, b, x_known

def forward_elimination(A, b):
    n = len(A)
    for i in range(n - 1):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    b[i], b[j] = b[j], b[i]
                    break
        for j in range(i + 1, n):
            if A[i][i] == 0:
                continue
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    return A, b

n = random.randint(1, 10)
A, b, x_known = generate_system(n)
print(A)

print(b)

print(x_known)
    