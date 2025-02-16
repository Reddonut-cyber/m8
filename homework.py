import numpy as np
import matplotlib.pyplot as plt

def parse_function_input(func_str, x):
    """Evaluate a user-provided function string."""
    return eval(func_str)

def read_points_from_file(filename):
    """Read 2D points from a file."""
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points

def solve_sle_interpolation(points):
    """Build interpolation polynomial by solving a system of linear equations."""
    n = len(points)
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    
    # Construct the Vandermonde matrix
    A = np.vander(x, N=n, increasing=True)
    
    # Solve the system A @ coeffs = y
    coeffs = np.linalg.solve(A, y)
    
    # Construct the polynomial
    return np.poly1d(coeffs[::-1])

def lagrange_basis(x, i, x_points):
    """Compute the i-th Lagrange basis polynomial."""
    basis = 1.0
    for j in range(len(x_points)):
        if j != i:
            basis *= (x - x_points[j]) / (x_points[i] - x_points[j])
    return basis

def lagrange_interpolation(points):
    """Build interpolation polynomial using Lagrange formula."""
    x_points = np.array([p[0] for p in points])
    y_points = np.array([p[1] for p in points])
    
    def poly(x):
        result = 0.0
        for i in range(len(x_points)):
            result += y_points[i] * lagrange_basis(x, i, x_points)
        return result
    
    return poly

def parametric_interpolation(points):
    """Build parametric interpolation polynomials (x(t) and y(t))."""
    t = np.arange(len(points))
    x_points = np.array([p[0] for p in points])
    y_points = np.array([p[1] for p in points])
    
    # Construct x(t) and y(t) using Lagrange interpolation
    def x_poly(t_val):
        result = 0.0
        for i in range(len(t)):
            result += x_points[i] * lagrange_basis(t_val, i, t)
        return result
    
    def y_poly(t_val):
        result = 0.0
        for i in range(len(t)):
            result += y_points[i] * lagrange_basis(t_val, i, t)
        return result
    
    return x_poly, y_poly

def plot_interpolation(points, polynomials, labels):
    """Plot the interpolation polynomials."""
    x_vals = np.linspace(min(p[0] for p in points), max(p[0] for p in points), 500)
    plt.figure()
    for poly, label in zip(polynomials, labels):
        if isinstance(poly, tuple):  # Parametric case
            t_vals = np.linspace(0, len(points) - 1, 500)
            x_vals = poly[0](t_vals)
            y_vals = poly[1](t_vals)
            plt.plot(x_vals, y_vals, label=label)
        else:  # Non-parametric case
            y_vals = [poly(x) for x in x_vals]
            plt.plot(x_vals, y_vals, label=label)
    plt.scatter([p[0] for p in points], [p[1] for p in points], color='red', label='Data Points')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interpolation Polynomials')
    plt.grid()
    plt.show()

def main():
    print("Interpolation Experimentation Tool")
    print("Choose input type:")
    print("1. Function and interval")
    print("2. File with 2D points")
    choice = int(input("Enter choice (1 or 2): "))

    if choice == 1:
        func_str = input("Enter function (e.g., 'x * np.sin(x) - x**2 + 1'): ")
        a = float(input("Enter interval start: "))
        b = float(input("Enter interval end: "))
        degree = int(input("Enter polynomial degree: "))
        x_vals = np.linspace(a, b, degree + 1)
        y_vals = parse_function_input(func_str, x_vals)
        points = list(zip(x_vals, y_vals))
    elif choice == 2:
        filename = input("Enter filename with points (e.g., 'points.txt'): ")
        points = read_points_from_file(filename)
        degree = len(points) - 1
    else:
        print("Invalid choice. Exiting.")
        return

    print("Choose interpolation approach(es):")
    print("1. Solve SLE")
    print("2. Lagrange formula")
    print("3. Parametric interpolation")
    approaches = list(map(int, input("Enter choices (e.g., '1 2 3'): ").split()))

    polynomials = []
    labels = []
    if 1 in approaches:
        poly_sle = solve_sle_interpolation(points)
        polynomials.append(poly_sle)
        labels.append("SLE Interpolation")
    if 2 in approaches:
        poly_lagrange = lagrange_interpolation(points)
        polynomials.append(poly_lagrange)
        labels.append("Lagrange Interpolation")
    if 3 in approaches:
        poly_x, poly_y = parametric_interpolation(points)
        polynomials.append((poly_x, poly_y))
        labels.append("Parametric Interpolation")

    plot_interpolation(points, polynomials, labels)

    while True:
        eval_point = input("Enter a point to evaluate the polynomial(s) (or 'exit' to quit): ")
        if eval_point.lower() == 'exit':
            break
        x = float(eval_point)
        for poly, label in zip(polynomials, labels):
            if isinstance(poly, tuple):  # Parametric case
                print(f"Cannot evaluate parametric interpolation at a specific x-value.")
            else:
                print(f"{label} at x = {x}: {poly(x)}")

if __name__ == "__main__":
    main()