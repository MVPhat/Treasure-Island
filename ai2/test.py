import numpy as np
import random

a = 1
b = 2

print(f"{a}{b}")

sus1 = "print(\'abc\')"

sus2 = "plus(a, b)"

def plus(a, b):
    return a + b

eval(sus1)

eval(sus2)