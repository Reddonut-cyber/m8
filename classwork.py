# linear regression

import numpy as np

def linear_regression(x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x ** 2)
    sum_xy = np.sum(x * y)
    
    # Calculate slope and intercept
    c1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    c0 = (sum_y - slope * sum_x) / n
    
    return slope, intercept

# Example usage

x = np.loadtxt('x_points.txt')
y = np.loadtxt('y_points.txt') 
              
c1, c0 = linear_regression(x, y)
print(f"Slope: {c1}")
print(f"Intercept: {c0}")

