import copy
from typing import Self


class Board:
	def __init__(self, matrix: list[list]):
		self.matrix = copy.deepcopy(matrix)

	def __eq__(self, other: Self):
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				if self.matrix[i][j] != other.matrix[i][j]: return False
		return True
	
	def __str__(self):
		string = ""
		for i in range(len(self.matrix)):
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
		boards = read_solutions(n, path)
		funds = fundamentals(boards)
		for b in range(len(funds)):
			for row in funds[b].matrix:
				for col in row:
					file.write(f"{col} ")
				file.write("\n")
			if b + 1 < len(funds):
				file.write("-----------------------------\n")
			else:
				file.write("-----------------------------")

def read_solutions(n, path: str):
	list_boards: list[Board] = []
	with open(f"{path}/{n}_queens.md", 'r') as file:
		string = file.read()
		str_boards = string.split("-----------------------------\n")
		for b in range(len(str_boards)):
			list_boards.append(Board([]))

			rows = str_boards[b].split("\n")[:-1:]
			for r in range(len(rows)):
				list_boards[b].matrix.append([])

				cols = rows[r].split(" ")
				for c in cols:
					list_boards[b].matrix[r].append(c)
	return list_boards

def fundamentals(og_boards):
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

def percentage(board_size, b, b2):
	return (100 * b + 10 * b2) / board_size

def solve(n):
	write_solutions(n, './src/other/queens/md')
	write_fundamentals(n, './src/other/queens/md')
	print(f"Check md folder for {n}_queens.md and {n}_fundamentals.md")

solve(13)