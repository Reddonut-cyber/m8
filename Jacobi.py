import random

def generate_random_system(n):
    

x0 = (0.8, 0.9)
x1, x2 = x0

def f1(x2):
    x1 = (3 - x2) / 2
    return  findx2(x1)

def f2(x1):
    x2 = (4 - x1) / 3
    return findx1(x2)

def findx1(x2):
    x1 = (3 - x2) / 2
    return x1

def findx2(x1):
    x2 = (4 - x1) / 3
    return x2