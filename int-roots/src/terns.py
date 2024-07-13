import copy
import datetime
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def rand_color():
	return (np.random.random(), np.random.random(), np.random.random(), 1)

def write_csv(content: str, filename: str, notify = False):
	with open(f"./data/csv/{filename}", "w") as fp:
		fp.write(content)
		if notify:
			print(f"{filename} written successfully!")

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

# https://stackoverflow.com/a/15285588
def is_prime(n):
  if n == 1 or n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  # since all primes > 3 are of the form 6n ± 1
  # start with f=5 (which is prime)
  # and test f, f+2 for being prime
  # then loop by 6. 
  f = 5
  while f <= r:
    # print('\t',f)
    if n % f == 0: return False
    if n % (f+2) == 0: return False
    f += 6
  return True

def terns(K: int, top: int = 1500):
	ab = []
	for _ in range(top):
		ab.append(top * [False])
	sln = copy.deepcopy(ab)

	csv = ""
	for a in range(1, 1 + top):
		for b in range(1, 1 + top):
			if a > b: continue
			gcd = mcd(a, b)
			if ab[(a // gcd) - 1][(b // gcd) - 1]: continue
			ab[a - 1][b - 1] = True
			c = math.dist([0, 0], [a, b]) / math.sqrt(K)
			if c == math.floor(c):
				sln[a - 1][b - 1] = True
				csv += f"{a},{b},{int(c)}\n"
	write_csv(csv, f"k{K}terns.csv", True)
	return sln

def plot():
	X = range(1, 100)
	Y = [n ** 2 for n in X]

	figure, axes = plt.subplots()
	plt.grid(True, "both")
	#plt.minorticks_on()
	#axes.yaxis.set_minor_locator(MultipleLocator(100))
	plt.xticks(X)
	plt.ylim(0, 50)

	color = rand_color()
	for line in Y:
		plt.plot(X, [line for _ in X], c=color)
	Y = [n ** 2 + 4 for n in X]
	plt.plot(X, Y, marker="o", c=rand_color())
	plt.show()

def image(ab, k):
	start = time.time()
	img = Image.new(mode = "RGB", size = (len(ab), len(ab)))

	for row in range(len(ab)):
		for col in range(len(ab)):
			if col < row:
				continue
			if ab[row][col - row]:
				img.putpixel((row, col), (95, 0, 159)) #hsv(row, col))
			print("\033c")
			print(f"{100 * round(row / len(ab) + col / (len(ab) ** 2), 5):.2f}%")
			print(f"{time.time() - start:.2f} s")
	DATE = datetime.datetime.now()
	DATE = str(DATE).replace(":", "-")
	img.save(f"./data/img/{DATE} - k{k}terns.png")

def main():
	for k in range(1, 1000):
		if is_prime(k):
			print(f"{k} ({k / 10:.2f}%)")
			matrix = terns(k)
			image(matrix, k)

if __name__ == "__main__":
	main()