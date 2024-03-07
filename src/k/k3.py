import math
from matplotlib.ticker import MultipleLocator
import numpy as np
import matplotlib.pyplot as plt


# https://stackoverflow.com/a/6800214
'''from functools import reduce
def factors(n):
    return reduce(list.__add__,
		([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)
	)'''

# https://www.w3resource.com/python-exercises/python-basic-exercise-31.php
# Define a function to calculate the greatest common divisor (MCD) of two numbers.
def mcd(x, y):
    # Initialize mcd to 1.
    mcd = 1
    
    # Check if y is a divisor of x (x is divisible by y).
    if x % y == 0:
        return y
    
    # Iterate from half of y down to 1.
    for k in range(int(y / 2), 0, -1):
        # Check if both x and y are divisible by k.
        if x % k == 0 and y % k == 0:
            # Update the MCD to the current value of k and exit the loop.
            mcd = k
            break
    
    # Return the calculated MCD.
    return mcd

def write_csv(content: str, filename: str, notify = False):
	with open(f"./data/csv/{filename}", "w") as fp:
		fp.write(content)
		if notify:
			print(f"{filename} written successfully!")

def rand_color():
	return (np.random.random(), np.random.random(), np.random.random(), 1)

TOP = 1500
matrix = []
for n in range(TOP):
	matrix.append(TOP * [False])
csv = ""
for i in range(1, 1 + TOP):
	for j in range(1, 1 + TOP):
		if i > j: continue
		gcd = mcd(i, j)
		if matrix[(i // gcd) - 1][(j // gcd) - 1]: continue
		matrix[i - 1][j - 1] = True
		dist = math.dist([0, 0], [i, j])
		if (dist / 3) == math.floor(dist / 3):
			csv += f"{i},{j},{int(dist)}\n"
	#print(i)
write_csv(csv, "k3terns.csv", True)