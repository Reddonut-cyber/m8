# import matplotlib.pyplot as plt
# import numpy as np

# h = 1
# k = 2

# r = 3

# # def x(t):
# #     return r * np.cos(t)

# # def y(t):
# #     return r * np.sin(t)

# def x(t):
#     return 16 * (np.sin(t) ** 3)

# def y(t):
#     return 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

# t_fine = np.linspace(0 , 2 * np.pi, 400)
# x_fine = x(t_fine)
# y_fine = y(t_fine)

# plt.figure(figsize=(8, 8))
# plt.plot(x_fine, y_fine, label='Circle', linewidth=2)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

def f1(t):
    return 16 * (np.sin(t) ** 3)

def f2(t):
    return 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

n = 90  # Number of points

a, b = 0, 2 * np.pi  # Interval for parameter t
t_values = np.linspace(a, b, n)  # Generate t values

# Compute x and y values based on the parametric equations
x_values = f1(t_values)
y_values = f2(t_values)

# Perform polynomial interpolation using numpy
coeff_x = np.polyfit(t_values, x_values, n-1)
coeff_y = np.polyfit(t_values, y_values, n-1)

poly_x = np.poly1d(coeff_x)
poly_y = np.poly1d(coeff_y)

t_fine = np.linspace(a, b, 100)
x_interp = poly_x(t_fine)
y_interp = poly_y(t_fine)

# Plot the results
plt.figure(figsize=(8, 8))
plt.plot(x_values, y_values, 'ro', label='Sample Points')
plt.plot(x_interp, y_interp, 'b-', label='Polynomial Interpolation')
plt.plot(np.cos(t_fine), np.sin(t_fine), 'g--', label='Actual Circle')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Parametric Interpolation of a Circle')
plt.axis('equal')
plt.grid()
plt.show()

