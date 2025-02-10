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

n = random.randint(1, 10)
A, b, x_known = generate_system(n)
print(A)

print(b)

print(x_known)
    