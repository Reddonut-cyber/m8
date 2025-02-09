from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import sympy as sp

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        func_str = request.form['function']
        a = float(request.form['a'])
        b = float(request.form['b'])
        tol = float(request.form['tol'])

        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        f_prime_expr = sp.diff(f_expr, x)
        f = sp.lambdify(x, f_expr, 'numpy')
        f_prime = sp.lambdify(x, f_prime_expr, 'numpy')

        
        g_expr = x - f_expr / f_prime_expr
        g = sp.lambdify(x, g_expr, 'numpy')

        newton_vals = newton_method(f, f_prime, (a + b) / 2, tol)
        bisection_vals = bisection_method(f, a, b, tol)
        fixed_vals = fixed_point_iteration(g, (a + b) / 2, tol)

        true_root = sp.nsolve(f_expr, x, (a + b) / 2)
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

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

        return render_template('index.html', plot_url=plot_url, 
                               newton_root=newton_vals[-1], newton_iters=len(newton_vals),
                               bisection_root=bisection_vals[-1], bisection_iters=len(bisection_vals),
                               fixed_root=fixed_vals[-1], fixed_iters=len(fixed_vals))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)