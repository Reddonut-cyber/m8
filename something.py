import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
data = np.genfromtxt("data.csv", delimiter=',')  # Load data assuming it's comma-separated

# Extract x and y values
x = data[:, 0]
y = data[:, 1]

# Define the function g(x) with the specified basis functions
def g(x, c):
    return c[0] + c[1] * np.cos(x) + c[2] * np.sin(x) + c[3] * x + c[4] * x**2 + c[5] * np.log(x)

# Set number of basis functions
N = 6  

# Construct matrix A
A = np.zeros((len(x), N))
b = y

for i in range(len(x)):
    A[i, 0] = 1  # c0
    A[i, 1] = np.cos(x[i])  # c1 * cos(x)
    A[i, 2] = np.sin(x[i])  # c2 * sin(x)
    A[i, 3] = x[i]  # c3 * x
    A[i, 4] = x[i] ** 2  # c4 * x^2
    A[i, 5] = np.log(x[i]) if x[i] > 0 else 0  # c5 * ln(x), avoid log(0)

# Solve for coefficients c
c = np.linalg.solve(A.T@A, A.T@b)

#print c
print(f"Co = {c}")

# Generate fine x values for plotting
x_fine = np.linspace(x.min(), x.max(), 400)
g_values = g(x_fine, c)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'ro', label="Data points")
plt.plot(x_fine, g_values, 'b-', label="Fitted function")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Curve fitting using specified basis functions")
plt.legend()
plt.grid()
plt.show()
