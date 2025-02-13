import numpy as np
import matplotlib.pyplot as plt

def interpolate_polynomial_sle(x, y):
    n = len(x)
    A = np.vander(x, increasing=True)
    coeffs = np.linalg.solve(A, y)
    return np.poly1d(coeffs[::-1])

def lagrange_polynomial(x, y):
    def L(k, x_val):
        terms = [(x_val - x[j]) / (x[k] - x[j]) for j in range(len(x)) if j != k]
        return np.prod(terms)
    
    def P(x_val):
        return sum(y[k] * L(k, x_val) for k in range(len(x)))
    
    return P

def plot_interpolation(func, title, a, b, n):
    x = np.linspace(a, b, n)
    y = func(x)
    
    poly_sle = interpolate_polynomial_sle(x, y)
    
    poly_lagrange = lagrange_polynomial(x, y)
    
    x_plot = np.linspace(a, b, 100)
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, func(x_plot), label='Original Function', linewidth=2)
    plt.plot(x_plot, poly_sle(x_plot), label='SLE Interpolation', linestyle='--')
    plt.plot(x_plot, [poly_lagrange(xi) for xi in x_plot], label='Lagrange Interpolation', linestyle='-.')
    plt.scatter(x, y, color='red', label='Interpolation Points')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'{title} on [{a}, {b}] with {n} Points')
    plt.grid(True)
    plt.show()

functions = [
    (lambda x: np.sin(x), 'sin(x)'),
    (lambda x: np.sin(3*x), 'sin(3x)'),
    (lambda x: np.sin(5*x), 'sin(5x)'),
    (lambda x: np.exp(x), 'exp(x)'),
    (lambda x: x**3, 'x^3'),
    (lambda x: np.cos(2*x), 'cos(2x)')
]

a, b = 0, 4
n_points = [3, 5, 7]

for func, title in functions:
    for n in n_points:
        plot_interpolation(func, title, a, b, n)