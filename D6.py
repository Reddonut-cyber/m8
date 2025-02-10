import random

def create_matrix(n):
    matrix = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    return matrix

n = random.randint(1, 10)
print(n)
print(f"{create_matrix(n)}")