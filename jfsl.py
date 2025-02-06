import math

def f(x):
    return x**2 - 5*x + 4

def df(x):
    return 2*x - 5

def newton_method(x0, epsilon=0.05, max_iter=100):
    x_prev = x0
    for i in range(max_iter):
        x_next = x_prev - f(x_prev) / df(x_prev)
        print(f"Iteration {i+1}: x = {x_next}")
        
        if abs(x_next - x_prev) < epsilon:
            return x_next, i+1
        
        x_prev = x_next
    
    return x_next, max_iter

x0 = 5
solution, iterations = newton_method(x0)
print(f"Solution: {solution} found in {iterations} iterations")