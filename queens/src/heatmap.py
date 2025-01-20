import pygame as pg
from pygame._sdl2 import Window
from typing import Tuple


class PyGame:
	def __init__(self, window_size: Tuple[int, int] = (1280, 720), caption: str = ""):
		pg.init()
		pg.font.init()
		self.FONT = pg.font.Font(size=24)

		self.window = pg.display.set_mode(window_size, pg.RESIZABLE)
		#Window.from_display_module().maximize()
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

		self.clicking = False
	
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

class Visualizer(PyGame):
	def __init__(self, cell_size: int = 50, caption: str = "", n: int = 8):
		super().__init__((n * cell_size - 1, n * cell_size - 1), caption)
		
		self.CELL_SIZE = cell_size
		matrix = []
		for _ in range(n):
			matrix.append([0 for _ in range(n)])
		self.matrix = matrix
		self.moves = [
			(-1, -1), (-1, 0), (-1, 1),
			(0, -1), (0, 1),
			(1, -1), (1, 0), (1, 1)
		]
		self.current_pos = (None, None)
		self.offset = (0, 0)

	def game(self):
		if pg.event.get(pg.MOUSEBUTTONDOWN):
			self.clicking = True
		if pg.event.get(pg.MOUSEBUTTONUP):
			self.clicking = False
			self.current_pos = (None, None)

		if self.clicking:
			mouse_pos = pg.mouse.get_pos()
			pos = (mouse_pos[0] // self.CELL_SIZE, mouse_pos[1] // self.CELL_SIZE)
			if self.is_valid_pos(pos) and pos != self.current_pos:
				if self.matrix[pos[0]][pos[1]] < 1:
					is_viable = True
					for move in self.moves:
						if not self.is_viable_pos(pos, move):
							is_viable = False
							break
					# Color only valid spots
					if is_viable: # or True:
						self.matrix[pos[0]][pos[1]] = 1
						for move in self.moves:
							self.heat_up((pos[0] + move[0], pos[1] + move[1]), move)
				else:
					self.matrix[pos[0]][pos[1]] = 0
					self.refresh()
				self.current_pos = pos
				

		stats = {str(i): 0 for i in range(6)}
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix)):
				rect = pg.rect.Rect(i * self.CELL_SIZE, j * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
				color = (0, 255, 0, 255 * self.matrix[i][j])
				pg.draw.rect(self.surfaces["bg"][0], (0, 255, 0, 255 * self.matrix[i][j]), rect)
				heat = self.FONT.render(f"{int(5 * self.matrix[i][j])}", True, color if self.matrix[i][j] < 1 else "magenta", "black")
				self.surfaces["fg"][0].blit(heat, heat.get_rect(center=rect.center))
				if self.matrix[i][j] >= 1:
					y45 = j - i
					y135 = j + i
					pg.draw.line(self.surfaces["bg"][2], "magenta", (
						0,
						y45 * self.CELL_SIZE
					), (
						len(self.matrix) * self.CELL_SIZE,
						(len(self.matrix) + y45) * self.CELL_SIZE
					), 2)
					pg.draw.line(self.surfaces["bg"][2], "magenta", (
						0,
						(y135 + 1) * self.CELL_SIZE
					), (
						(y135 + 1) * self.CELL_SIZE,
						0
					), 2)
					""" pg.draw.line(self.surfaces["bg"][2], "magenta", (
						(i + 0.5) * self.CELL_SIZE,
						0
					), (
						(i + 0.5) * self.CELL_SIZE,
						self.window.get_rect().h
					), 2)
					pg.draw.line(self.surfaces["bg"][2], "magenta", (
						0,
						(j + 0.5) * self.CELL_SIZE
					), (
						self.window.get_rect().w,
						(j + 0.5) * self.CELL_SIZE
					), 2) """
				stats[str(int(5 * self.matrix[i][j]))] += 1
		pg.draw.rect(self.surfaces["fg"][2], (0, 0, 0, 127), self.window.get_rect())
		txt_offset = self.FONT.render(f"{self.offset}", True, "purple", "black")
		self.surfaces["fg"][2].blit(txt_offset, txt_offset.get_rect(centerx=self.window.get_rect().centerx))
		txt_stats = self.FONT.render(f"{stats}", True, "purple", "black")
		self.surfaces["fg"][2].blit(txt_stats, (txt_stats.get_rect(centerx=self.window.get_rect().centerx).x, txt_stats.get_rect().bottom))

	def refresh(self):
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix)):
				if self.matrix[i][j] < 1:
					self.matrix[i][j] = 0
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix)):
				if self.matrix[i][j] == 1:
					for move in self.moves:
						self.heat_up((i + move[0], j + move[1]), move)
				

	def heat_up(self, pos: tuple[int], move: tuple[int]):
		if self.is_valid_pos(pos):
			if (self.matrix[pos[0]][pos[1]] <= 0.8):
				self.matrix[pos[0]][pos[1]] += 0.2
				self.heat_up((pos[0] + move[0], pos[1] + move[1]), move)

	def is_valid_pos(self, pos: tuple[int]):
		return (
			0 <= pos[0] < len(self.matrix) and
			0 <= pos[1] < len(self.matrix)
		)

	def is_viable_pos(self, pos: tuple[int], move: tuple):
		if self.is_valid_pos(pos):
			if self.matrix[pos[0]][pos[1]] < 1:
				return self.is_viable_pos((pos[0] + move[0], pos[1] + move[1]), move)
			return False
		return True

def main():
	v = Visualizer(caption="N Queens", n=19, cell_size=50)
	v.run()

if __name__ == "__main__":
	main()