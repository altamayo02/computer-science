import datetime
import colorsys
import math
import time
from enum import Enum
from PIL import Image


class Color(Enum):
	PURPLE = (95, 0, 159)
	GREEN = (0, 63, 0)
	WHITE = (255, 255, 255)

DATE = datetime.datetime.now()
DATE = str(DATE).replace(":", "-")
TIME = time.time()

def semidist(n1, n2):
	return n1 ** 2 + n2 ** 2

def hsv(n1, n2):
	hsv = [int(255 * num) for num in colorsys.hsv_to_rgb((semidist(n1, n2) / 127) % 1.0, 1, 1)]
	return tuple(hsv)

# https://stackoverflow.com/a/15285588
def is_prime(n):
  if n == 2 or n == 3: return True
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


SIZE = 100

plot = []
for n1 in range(1, 1 + SIZE):
	plot.append([])
	for n2 in range(1, 1 + SIZE):
		if n2 < n1: continue
		prime = is_prime(semidist(n1, n2))
		if n1 % 100 == 0:
			print(f"{n1} ** 2 + {n2} ** 2 = {semidist(n1, n2)}")
		plot[n1 - 1].append(prime)

img = Image.new(mode = "RGB", size = (SIZE, SIZE))

for n in range(1, SIZE):
	if is_prime(n):
		for theta in range(45):
			# TODO - Fix polar grid
			img.putpixel((round(n * math.cos(theta)), round(n * math.sin(theta))), Color.GREEN.value) #hsv(row, col))
			pass

for row in range(SIZE):
	for col in range(SIZE):
		if col < row:
			continue
		if plot[row][col - row]:
			img.putpixel((row, col), Color.PURPLE.value) #hsv(row, col))
		print("\033c")
		print(f"{100 * round(row / SIZE + col / (SIZE ** 2), 5)}%")
		print(f"{time.time() - TIME} s")

img.save(f"./data/img/{DATE}.png")
print("\nImage saved.")