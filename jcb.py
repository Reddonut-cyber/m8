import random
import math
import matplotlib.pyplot as plt

def vector_norm(v):
    return math.sqrt(sum(x * x for x in v))

def vector_subtract(v, w):
    return [v[i] - w[i] for i in range(len(v))]

def generate_diagonally_dominant_matrix(n):
    A = []
    for i in range(n):
        row = [random.uniform(0, 1) for _ in range(n)]
        sum_off_diag = sum(abs(row[j]) for j in range(n) if j != i)
        row[i] = sum_off_diag + random.uniform(1, 2)
        A.append(row)
    return A

def generate_random_vector(n, low=0.0, high=1.0):
    return [random.uniform(low, high) for _ in range(n)]

def matrix_vector_mult(A, x):
    n = len(A)
    b = []
    for i in range(n):
        s = 0.0
        for j in range(len(x)):
            s += A[i][j] * x[j]
        b.append(s)
    return b

def jacobi(A, b, x0, tol=1e-6, max_iter=50, x_exact=None):
    n = len(b)
    x = x0[:]  
    errors = []
    print("Jacobi Iterations:")
    for it in range(max_iter):
        x_new = [0.0] * n
        for i in range(n):
            s = 0.0
            for j in range(n):
                if j != i:
                    s += A[i][j] * x[j]
            x_new[i] = (b[i] - s) / A[i][i]
        diff = vector_norm(vector_subtract(x_new, x))
        if x_exact is not None:
            err = vector_norm(vector_subtract(x_new, x_exact))
        else:
            err = diff
        errors.append(err)
        print(f"Iteration {it+1}: {x_new}, diff = {diff}")
        if diff < tol:
            print("Jacobi: Convergence reached!")
            break
        x = x_new[:]
    return x, errors

def gauss_seidel(A, b, x0, tol=1e-6, max_iter=50, x_exact=None):
    n = len(b)
    x = x0[:]  
    errors = []
    print("\nGauss-Seidel Iterations:")
    for it in range(max_iter):
        x_old = x[:]  
        for i in range(n):
            s = 0.0
            for j in range(i):
                s += A[i][j] * x[j]
            for j in range(i+1, n):
                s += A[i][j] * x_old[j]
            x[i] = (b[i] - s) / A[i][i]
        diff = vector_norm(vector_subtract(x, x_old))
        if x_exact is not None:
            err = vector_norm(vector_subtract(x, x_exact))
        else:
            err = diff
        errors.append(err)
        print(f"Iteration {it+1}: {x}, diff = {diff}")
        if diff < tol:
            print("Gauss-Seidel: Convergence reached!")
            break
    return x, errors

def main():
    n = random.randint(3, 10)
    print("Matrix size n =", n)
    
    A = generate_diagonally_dominant_matrix(n)
    print("\nGenerated matrix A:")
    for row in A:
        print(row)
        
    x_exact = generate_random_vector(n, 0, 10)
    print("\nExact solution x_exact:")
    print(x_exact)
    
    b = matrix_vector_mult(A, x_exact)
    print("\nRight-hand side vector b:")
    print(b)
    
    x0 = [x_exact[i] + random.uniform(-0.5, 0.5) for i in range(n)]
    print("\nInitial guess x0:")
    print(x0)
    
    max_iterations = 10
    x_jacobi, errors_jacobi = jacobi(A, b, x0, tol=1e-6, max_iter=max_iterations, x_exact=x_exact)
    
    x_gs, errors_gs = gauss_seidel(A, b, x0, tol=1e-6, max_iter=max_iterations, x_exact=x_exact)
    
    iterations_j = list(range(1, len(errors_jacobi) + 1))
    iterations_g = list(range(1, len(errors_gs) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(iterations_j, errors_jacobi, marker='o', label="Jacobi")
    plt.plot(iterations_g, errors_gs, marker='s', label="Gauss-Seidel")
    plt.xlabel("Iteration")
    plt.ylabel("Error (Euclidean norm)")
    plt.title("Convergence Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
