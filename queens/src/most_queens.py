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
		text = self.FONT.render("game() is not yet implemented", True, "purple")
		self.window.blit(text, text.get_rect(center=self.window.get_rect().center))

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

class MostQueens(PyGame):
	def __init__(self, board_size, window_size: Tuple[int, int] = (1280, 720), caption: str = ""):
		super().__init__(window_size, caption)

		self.CELL_SIZE = 200
		self.BOARD_SIZE = board_size
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
	
	def is_valid(self, i, j):
		is_valid = 0 <= i < len(self.board)
		if not is_valid: return False
		is_valid = is_valid and 0 <= j < len(self.board[i])
		return is_valid
	
	def game(self):
		pass
	
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
	game = MostQueens(8, caption="Most Queens")
	game.run()