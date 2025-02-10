import random

def generate_random_system(n):
    A  = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    x_known = [i + 1 for i in range(n)]
    b = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += A[i][j] * x_known[j]
        b.append(s)
    return A, b, x_known

def generate_hilbert_system(n):
    A = [[1/(i + j + 1) for j in range(n)] for i in range(n)]
    x_known = [i + 1 for i in range(n)]
    b = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += A[i][j] * x_known[j]
        b.append(s)
    return A, b, x_known

def print_augmented_matrix(A, b):
    n = len(A)
    for i in range(n):
        row_str = " ".join(f"{A[i][j]:7.2f}" for j in range(n))
        print(f"{row_str} | {b[i]:7.2f}")
    print()

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
        print(f"After eliminating column {i}:")
        print_augmented_matrix(A, b)
    return A, b
    
def backward_substitution(A, b):
    n = len(A)
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_ax = 0
        for j in range(i+1, n):
            sum_ax += A[i][j] * x[j]
        if A[i][i] == 0:
            raise ZeroDivisionError("pivot = 0 in backward substitution")
        x[i] = (b[i] - sum_ax) / A[i][i]
    return x

def compute_residue(A, b, x):
    """
    Compute the residue vector r = Ax - b.
    """
    n = len(A)
    residue = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += A[i][j] * x[j]
        residue.append(s - b[i])
    return residue

def test_system(system_type, n):
    print(f"Testing {system_type} system of size n = {n}")
    
    if system_type == "random":
        A, b, x_known = generate_random_system(n)
    elif system_type == "hilbert":
        A, b, x_known = generate_hilbert_system(n)
    else:
        raise ValueError("Unknown system type")
    
    print("Known solution x:", x_known)
    print("Initial augmented matrix [A|b]:")
    print_augmented_matrix(A, b)
    
    A_copy = [row[:] for row in A]
    b_copy = b[:]
    A_upper, b_upper = forward_elimination(A_copy, b_copy)
    
    x_computed = backward_substitution(A_upper, b_upper)
    print("Computed solution x:", x_computed)
    
    residue = compute_residue(A, b, x_computed)
    print("Residue vector (Ax - b):", residue)
    max_error = max(abs(r) for r in residue)
    print("Maximum residue error:", max_error)
    print("=" * 60, "\n")

def main():
    sizes = [5, 10, 20]
    for n in sizes:
        test_system("random", n)
        test_system("hilbert", n)

if __name__ == "__main__":
    main()