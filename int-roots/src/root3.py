import math
import datetime
from PIL import Image

RED = "\u001b[31m"
DEFAULT = "\u001b[0m"

mat = []
R = 570
for i in range(R):
	mat.append([])
	for _ in range(R):
		mat[i].append(0)
#SIZE = 64

moves = [
	(0, 3), (3, 3)
]

def is_valid(K, n1, n2):
	return n1 ** 2 + n2 ** 2 <= K ** 2

def is_viable(sln, n1, n2):
	return sln[int(n1 / 3) - 1][int(n2 / 3) - 1] == 0

# K = 35
def backtrack(sln: list, K: int = R, n1: int = 1, n2: int = 1):
	if is_valid(K, n1, n2):
		if is_viable(sln, n1, n2):
			sln[int(n1 / 3) - 1][int(n2 / 3) - 1] = 1
			dist = n1 ** 2 + n2 ** 2
			#if 3 * K ** 2 < dist:
			#    print(f"({n1**2}, {n2**2}): {dist == K * math.sqrt(3)} ({dist})")
			if dist == K ** 2:
				return dist
			else:
				for move in moves:
					backtrack(sln, K, n1 + move[0], n2 + move[1])
			#print("---------------")
		#print("---------------")

def exec():
	backtrack(mat)
	#print_matrix(mat)
	print("***************")
	date = datetime.datetime.now()
	img = Image.new(mode = "RGB", size = (R+1, R+1))
	for row in range(len(mat)):
		for col in range(len(mat[0])):
			if mat[row][col]:
				img.putpixel((row + 1, col + 1), (255, 255, 255))
	date = str(date).replace(":", "-")
	img.save(f"./data/img/{date}.png")
	print("Image saved.")
	

def to_string(m):
	string = ""
	for row in m:
		for num in row:
			string += f"{num};"
			#string += f"{RED if num == 1 else ''}{num}{DEFAULT if num == 1 else ''} "
		string += "\n"
	return string