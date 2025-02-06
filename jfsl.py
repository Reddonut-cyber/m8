import random
import math

def f(x):
    return x**2 - (5*x) + 4

def dif(x):
    return 2*x - 5

def g(num):
    for i in range(100):
        x = num - f(num)/dif(num)
        if abs(x - num) < 0.01:
            break
        print(f"{i}==={x}")
        num = x
        

    

num = 5
g(num)