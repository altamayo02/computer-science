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

board = Board([
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0]
])

moves = [
	(0, 0), (0, 1), (0, 2),
	(1, 0), (1, 1), (1, 2),
	(2, 0), (2, 1), (2, 2)
]

def is_valid(board: Board, move: tuple[int, int]):
	return (
		0 <= move[0] < len(board.matrix) and
		0 <= move[1] < len(board.matrix[0])
	)

def is_viable(board: Board, move: tuple[int, int]):
	return board.matrix[move[0]][move[1]] == 0

def game_ended(board: Board):
	""" for row in board:
		if abs(sum(row)) == 3: return True
	for val in range(len(board[0])):
		column = []
		for row in range(len(board)):
			column.append(board[row][val])
		if abs(sum(column)) == 3: return True
	diag = []
	for i in range(len(board)):
		diag.append(board[i][i])
	if abs(sum(diag)) == 3: return True
	diag = []
	for i in range(len(board)):
		diag.append(board[i][len(board) - 1 - i])
	if abs(sum(diag)) == 3: return True """
	
	num_moves = 0
	for row in board.matrix:
		for val in row:
			if val != 0: num_moves += 1
	return num_moves == 9

def backtrack(board: Board, value: int = 1, sol: list[Board] = []):
	if game_ended(board):
		sol.append(board)
		return
	for move in moves:
		if is_valid(board, move) and is_viable(board, move):
			child_board = Board(board.matrix)
			child_board.matrix[move[0]][move[1]] = value
			backtrack(child_board, -1 * value)
	return sol

def print_sol(sol):
	for table in sol:
		for row in table:
			print(row)
		print("---------------")
	print("---------------")
	print("---------------")

def identify(boards: list[Board]):
	"""
	Filters out duplicate boards. Useful for identifying fundamentals.
	"""

	fundamentals: list[Board] = []
	for board in boards:
		if board not in fundamentals:
			fundamentals.append(board)
	return fundamentals

games = backtrack(board)
fundamentals = identify(games)
for f in fundamentals:
	for row in f.matrix:
		for val in row:
			print({
				-1: 'O',
				1: 'X'
			}[val], end=' ')
		print()
	print("---------------")

print(len(games))
print(len(fundamentals))