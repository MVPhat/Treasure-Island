import numpy as np
import random

a = np.array(list(range(16)), dtype=np.int8)
a = a.reshape((4, 4))

a = (a == 5)

print(a)  