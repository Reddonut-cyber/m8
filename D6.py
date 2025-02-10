import random

def create_matrix(n):
    matrix = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    return matrix
def forward_elimination(n):
    matrix = create_matrix(n)
    for i in range(n - 1):
        if matrix[i][i] == 0:
            swapped = False
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    swapped = True
                    break
            if not swapped:
                print(f"Warning: Pivot at row {i} is zero and cannot be swapped.")
                continue  
        
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

n = random.randint(1, 10)
print(n)
result_matrix = forward_elimination(n)
for row in result_matrix:
    print(row)