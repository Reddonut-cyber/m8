import random

def create_matrix(n):
    matrix = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    return matrix
def forward_elimination():
    matrix = create_matrix(n)
    for i in range(n - 1):
        for j in range(i + 1, n):
            print(matrix)
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

n = random.randint(1, 10)
print(n)
print(f"{forward_elimination()}")