import datetime
import colorsys
from math import dist
from PIL import Image

SIZE = 10000
PURPLE = (95, 0, 159)
RED = (0, 31, 0)

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

plot = []
for n1 in range(1, 1 + SIZE):
	plot.append([])
	for n2 in range(1, 1 + SIZE):
		if n2 < n1: continue
		prime = is_prime(semidist(n1, n2))
		if n1 % 10 == 0:
			print(f"{n1} ** 2 + {n2} ** 2 = {semidist(n1, n2)}")
		plot[n1 - 1].append(prime)

date = datetime.datetime.now()
date = str(date).replace(":", "-")
img = Image.new(mode = "RGB", size = (SIZE + 1, SIZE + 1))
for row in range(len(plot)):
	for col in range(len(plot[0])):
		if col < row:
			continue
		# TODO - This is super wrong - prime check is with distance squared, not distance itself (e.g. (3, 4) = |5|)
		if plot[row][col - row] and is_prime(round(dist([0, 0], [row, col]))):
			img.putpixel((row, col), (255, 255, 255)) #hsv(row, col))
		elif plot[row][col - row]:
			img.putpixel((row, col), PURPLE) #hsv(row, col))
		elif is_prime(round(dist([0, 0], [row, col]))):
			img.putpixel((row, col), RED) #hsv(row, col))

img.save(f"./data/img/{date}.png")
print("Image saved.")