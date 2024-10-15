import copy
from typing import Self


class Board:
	def __init__(self, matrix: list[list]):
		self.matrix = copy.deepcopy(matrix)

	def rotate_cw(self):
		rotated: list[list] = []
		for i in range(len(self.matrix)):
			rotated.append([])
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix)):
				rotated[len(self.matrix) - 1 - j].append(self.matrix[i][j])
		self.matrix = rotated

	def mirror(self):
		mirrored: list[list] = []
		for i in range(len(self.matrix)):
			mirrored.append([])
			for j in range(len(self.matrix)):
				mirrored[i].append(self.matrix[i][len(self.matrix) - 1 - j])
		self.matrix = mirrored

	def translate(self, i0: int, j0: int):
		translated: list[list] = []
		for i in range(len(self.matrix)):
			translated.append([])
			for j in range(len(self.matrix)):
				translated[i].append(self.matrix[(i + i0) % len(self.matrix)][(j + j0) % len(self.matrix)])
		self.matrix = translated

	def __eq__(self, other: Self):
		def component_eq(other: Self):
			for i in range(len(self.matrix)):
				for j in range(len(self.matrix[i])):
					if self.matrix[i][j] != other.matrix[i][j]: return False
			return True
		
		dummy = copy.deepcopy(other)
		for _ in range(2):
			if component_eq(dummy): return True
			for _ in range(3):
				dummy.rotate_cw()
				if component_eq(dummy):
					return True
			dummy.mirror()
		return False
	
	def __str__(self):
		string = ""
		for i in range(len(self.matrix) - 1, -1, -1):
			string += f'{" ".join(self.matrix[i])}\n'
		string += "-----------------------------"
		return string

def rotate(board):
	board: Board = board

	rotated: list[list] = []
	for row in range(len(board.matrix)):
		rotated.append([])
	for row in range(len(board.matrix)):
		for col in range(len(board.matrix)):
			rotated[len(board.matrix) - 1 - col].append(board.matrix[row][col])
	return Board(rotated)

def mirror(board):
	board: Board = board

	mirrored: list[list] = []
	for row in range(len(board.matrix)):
		mirrored.append([])
		for col in range(len(board.matrix)):
			mirrored[row].append(board.matrix[row][len(board.matrix) - 1 - col])
	return Board(mirrored)

# Thanks cmc!
# https://leetcode.com/problems/n-queens/solutions/19810/fast-short-and-easy-to-understand-python-solution-11-lines-76ms
def solve_board(n):
	def DFS(queens, xy_dif, xy_sum):
		p = len(queens)
		if p==n:
			result.append(queens)
			return None
		for q in range(n):
			if q not in queens and p-q not in xy_dif and p+q not in xy_sum: 
				DFS(queens+[q], xy_dif+[p-q], xy_sum+[p+q])  
	result = []
	DFS([],[],[])
	return [ [". "*i + "Q" + " ."*(n-i-1) for i in sol] for sol in result]

def write_solutions(n, path: str):
	with open(f"{path}/{n}_queens.md", 'w') as file:
		boards = solve_board(n)
		for b in range(len(boards)):
			for row in boards[b]:
				file.write(f"{row}\n")
			if b + 1 < len(boards):
				file.write("-----------------------------\n")
			else:
				file.write("-----------------------------")

def write_fundamentals(n, path: str):
	with open(f"{path}/{n}_fundamentals.md", 'w') as file:
		boards = read_boards(n, path)
		funds = deduplicate(boards)
		for b in range(len(funds)):
			for row in funds[b].matrix:
				for col in row:
					file.write(f"{col} ")
				file.write("\n")
			if b + 1 < len(funds):
				file.write("-----------------------------\n")
			else:
				file.write("-----------------------------")

def read_boards(n, path: str, fundamentals = False):
	list_boards: list[Board] = []

	suffix ="queens"
	if fundamentals:
		suffix = "fundamentals"

	with open(f"{path}/{n}_{suffix}.md", 'r') as file:
		string = file.read()
		str_boards = string.split("-----------------------------\n")
		for b in range(len(str_boards)):
			list_boards.append(Board([]))

			rows = str_boards[b].split("\n")[:-1:]
			for r in range(len(rows)):
				list_boards[b].matrix.append([])

				cols = rows[r].strip().split(" ")
				for c in cols:
					list_boards[b].matrix[r].append(c)
	return list_boards

# What the hell was I doing?
def fundamentals(og_boards):
	"""
		Unused function
	"""
	
	def percentage(board_size, b, b2):
		return (100 * b + 10 * b2) / board_size

	boards: list[Board] = copy.deepcopy(og_boards)
	b = 0
	while b < len(boards):
		# Mirror of the current board
		for b2 in range(len(boards)):
			# Verbose
			perc = percentage(len(boards), b, 0.25 * b2)
			print(f"{perc:.10f}%")
			if b == b2: continue
			if mirror(boards[b2]) == boards[b]:
				del boards[b2]
				if b >= len(boards): return boards
				break
		temp_board = boards[b]
		for i in range(3):
			temp_board = rotate(temp_board)
			for b2 in range(len(boards)):
				perc = percentage(len(boards), b, (i + 2) * 0.25 * b2)
				print(f"{perc:.10f}%")
				if b == b2: continue
				# Rotation of the current board
				if boards[b2] == temp_board:
					# print(boards[b2] == temp_board)
					# print(mirror(boards[b2]) == temp_board)
					del boards[b2]
					if b >= len(boards): return boards
					break
			for b2 in range(len(boards)):
				if b == b2: continue
				# Mirror of the rotation of the current board
				if mirror(boards[b2]) == temp_board:
					del boards[b2]
					if b >= len(boards): return boards
					break
		b += 1
	
	return boards

def deduplicate(boards: list[Board]):
	"""
	Filters out duplicate boards. Useful for identifying fundamentals.
	"""

	fundamentals = []
	for board in boards:
		if board not in fundamentals:
			fundamentals.append(board)
	return fundamentals

def solve(n):
	write_solutions(n, './data/md')
	write_fundamentals(n, './data/md')
	print(f"Check md folder for {n}_queens.md and {n}_fundamentals.md")

def is_solution(board: Board):
	boards = read_boards(len(board.matrix), './data/md')
	return board in boards

def permutate(board: Board, i1: int, i2: int):
	permutated = copy.deepcopy(board)
	permutated.matrix[i1], permutated.matrix[i2] = board.matrix[i2], board.matrix[i1]
	return permutated

def translate(board: Board, i0: int, j0: int):
	translated = copy.deepcopy(board)
	for i in range(len(board.matrix)):
		for j in range(len(board.matrix)):
			translated.matrix[i][j] = board.matrix[(i + i0) % len(board.matrix)][(j + j0) % len(board.matrix)]
	return translated

def analyze(board: Board):
	solutions = []
	for i1 in range(len(board.matrix)):
		for i2 in range(i1 + 1, len(board.matrix)):
			#if not (i1 == 0 and i2 == 2): continue
			permutated = permutate(board, i1, i2)
			for i0 in range(len(permutated.matrix)):
				for j0 in range(len(permutated.matrix)):
					translated = translate(permutated, i0, j0)
					if is_solution(translated):
						#print(f'\t{i1 + 1}, {i2 + 1}')
						print(f'\ti1: {i1 + 1}, i2: {i2 + 1}; i0: {i0}, j0: {j0}')
						"""
						print(translated)
						print(f"IS A SOLUTION\n")
						"""
						if translated not in solutions:
							#print(translated)
							solutions.append(translated)
	return solutions

test = read_boards(7, './data/md', True)[1]
"""
test = read_boards(8, './data/md', True)[1]
test.rotate_cw()
test.rotate_cw()
test.rotate_cw()
"""
#test = read_boards(9, './data/md', True)[0]

boards = [test]
for b in boards:
	print(f"Current stack size: {len(boards)}")
	print()
	print("CURRENTLY ANALYZING:")
	print(b)
	analyzed = analyze(b)
	print("GOT:")
	for a in analyzed:
		print(a)
	print()
	if len(analyzed) > 0:
		new = []
		for board in analyzed:
			if board not in boards:
				new.append(board)
		
		if len(new) > 0:
			boards += new
	else:
		print("FUCK!")
		break