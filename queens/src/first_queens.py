import pygame as pg
from pygame._sdl2 import Window
from typing import Tuple


class PyGame:
	def __init__(self, window_size: Tuple[int, int] = (1280, 720), caption: str = ""):
		pg.init()
		pg.font.init()
		self.FONT = pg.font.Font(size=24)

		self.window = pg.display.set_mode(window_size, pg.RESIZABLE)
		Window.from_display_module().maximize()
		self.surfaces = {
			"bg": [
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA)
			],
			"fg": [
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA)
			]
		}
		self.clock = pg.time.Clock()
		self.lifespan = self.clock.tick()
		self.is_running = True
		self.is_paused = False
		if caption: pg.display.set_caption(caption)
	
	def game(self):
		raise Exception("game() is not yet implemented.")

	def run(self):
		while self.is_running:
			# If window is prompted to close
			if pg.event.get(pg.QUIT):
				self.is_running = False

			# Clear the canvas
			for layer in self.surfaces:
				for n in self.surfaces[layer]:
					n.fill((255, 255, 255, 0))
			self.window.fill("black")

			# Game logic
			self.game()
			
			# Update the canvas
			for layer in self.surfaces:
				for n in self.surfaces[layer]:
					self.window.blit(n, (0, 0))
			pg.display.update()

			if not self.is_paused:
				self.clock.tick()
				self.lifespan += self.clock.get_time()
			elif pg.event.get(pg.MOUSEBUTTONUP):
				self.is_paused = False
		pg.quit()

class FirstQueens(PyGame):
	def __init__(self, window_size: Tuple[int, int] = (1280, 720), caption: str = ""):
		super().__init__(window_size, caption)

		self.CELL_SIZE = 20
		self.MOVES = [
			(-1, -1), (-1, 0), (-1, 1),
			(0, -1), (0, 1),
			(1, -1), (1, 0), (1, 1)
		]
		self.BOARD_UPDATE = pg.USEREVENT
		# FIXME - This is called before board is updated- big trouble
		pg.time.set_timer(self.BOARD_UPDATE, 1000)

		self.queens: list[list] = [(0, 0)]
		self.board: list[list] = [[2]]
		self.position = 0
		self.velocity = 0.05


	def game(self):
		# Pause game if click occurs
		if pg.event.get(pg.MOUSEBUTTONUP):
			self.is_paused = True

		self.position += self.clock.get_time() * self.velocity
		board_size = int(self.position / self.CELL_SIZE)
		
		# Update board
		if pg.event.get(self.BOARD_UPDATE):
			def mark(i, j):
				self.board[i][j] = 2
				for m in self.MOVES:
					i1 = m[0]
					j1 = m[1]
					while self.is_valid(i + i1, j + j1):
						if self.board[i + i1][j + j1] == 0:
							self.board[i + i1][j + j1] = 1
						i1 += m[0]
						j1 += m[1]
			
			for i in range(board_size):
				self.board.append([])
				for j in range(board_size):
					self.board[i].append(0)
			
			for q in self.queens:
				i, j = q[0], q[1]
				mark(i, j)

			#print(self)

			for i in range(board_size):
				for j in range(board_size):
					# Personal preference
					#if self.board[i][j] == 0:
					if self.board[j][i] == 0:
						self.queens.append((j, i))
						mark(j, i)

		# Draw grid
		for i in range(board_size + 1):
			for j in range(board_size + 1):
				# Personal preference
				#if self.is_valid(i, j):
				if self.is_valid(j, i):
					if i != board_size and j != board_size:
						col = {
							0: "lime",
							1: "coral",
							2: "purple"
						}[self.board[j][i]]
						rect = pg.rect.Rect(i * self.CELL_SIZE, j * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
						pg.draw.rect(self.surfaces["bg"][0], col, rect)
						font = self.FONT.render(f"{(max(i, j) + 1) % 10}", True, "black")
						self.surfaces["fg"][0].blit(font, font.get_rect(center=rect.center))
				if i == 0:
					# Trippy!
					#pg.draw.line(self.surfaces["bg"][1], "white", (10 * (j - 1), 0), (10 * j, 10 * (BOARD_SIZE - 1)))
					x = j * self.CELL_SIZE
					y = board_size * self.CELL_SIZE
					div10 = j % 10 == 0
					pg.draw.line(self.surfaces["bg"][1], "white" if not div10 else "teal", (x, 0), (x, y), 3 if div10 else 1)
			div10 = i % 10 == 0
			pg.draw.line(
				self.surfaces["bg"][1 if not div10 else 2],
				"white" if not div10 else "teal",
				(0, i * self.CELL_SIZE),
				(board_size * self.CELL_SIZE, i * self.CELL_SIZE),
				3 if div10 else 1
			)

		# Draw scope
		pg.draw.rect(
			self.surfaces["fg"][-1],
			["teal", "purple", "coral", "deeppink"][board_size % 4],
			pg.Rect(-1, -1, self.position + 1, self.position + 1),
			3
		)

	def is_valid(self, i, j):
		is_valid = 0 <= i < len(self.board)
		if not is_valid: return False
		is_valid = is_valid and 0 <= j < len(self.board[i])
		return is_valid
	
	def __str__(self):
		for r in self.board:
			for c in r:
				col = {
					0: 32,
					1: 31,
					2: 35
				}[c]

				print(f"\u001B[{col}m{c}", end=" ")
			print()
		print("\u001B[0m---------------")

if __name__ == "__main__":
	game = FirstQueens(caption="First Queens")
	game.run()