import random
import math

def f1(x):
    return (x**2)-2

def f2(x):
    return math.sqrt(x+2)

def f3(x):
    return (x+2)/2

def f4(x):
    return -(1/6) * ((x**2) - x - 2) + x
def g(num):
    for i in range(100):
        x = f4(num)
        if (x - num) < 1e-16:
            break
        print(f"{i}==={x}")
        num = x
    

num = random.uniform(1, 3)
g(num)