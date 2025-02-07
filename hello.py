import numpy as np
import matplotlib.pyplot as plt

def newton_method(f, f_prime, x0, tol=1e-6, max_iter=50):
    x_vals = [x0]
    for _ in range(max_iter):
        if abs(f_prime(x0)) < 1e-10:
            break  
        x0 = x0 - f(x0) / f_prime(x0)
        x_vals.append(x0)
        if abs(f(x0)) < tol:
            break
    return x_vals

def bisection_method(f, a, b, tol=1e-6, max_iter=50):
    if f(a) * f(b) > 0:
        return []  
    x_vals = []
    for _ in range(max_iter):
        c = (a + b) / 2
        x_vals.append(c)
        if abs(f(c)) < tol:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return x_vals

def fixed_point_iteration(g, x0, tol=1e-6, max_iter=50):
    x_vals = [x0]
    for _ in range(max_iter):
        x1 = g(x0)
        x_vals.append(x1)
        if abs(x1 - x0) < tol:
            break
        x0 = x1
    return x_vals


def f(x):
    return x**2 - 2

def f_prime(x):
    return 2 * x

def g(x):
    return (x + 2 / x) / 2


x0_newton = 1.5  
a_bisection, b_bisection = 0, 2  
x0_fixed = 1.5  


newton_vals = newton_method(f, f_prime, x0_newton)
bisection_vals = bisection_method(f, a_bisection, b_bisection)
fixed_vals = fixed_point_iteration(g, x0_fixed)

true_root = np.sqrt(2)
newton_errors = [abs(x - true_root) for x in newton_vals]
bisection_errors = [abs(x - true_root) for x in bisection_vals]
fixed_errors = [abs(x - true_root) for x in fixed_vals]


plt.figure(figsize=(8, 6))
plt.plot(range(len(newton_errors)), newton_errors, label='Newton', marker='o')
plt.plot(range(len(bisection_errors)), bisection_errors, label='Bisection', marker='s')
plt.plot(range(len(fixed_errors)), fixed_errors, label='Fixed Point', marker='^')
plt.yscale('log')
plt.xlabel('Iteration')
plt.ylabel('Error')
plt.title('Convergence of Root-Finding Methods')
plt.legend()
plt.show()
