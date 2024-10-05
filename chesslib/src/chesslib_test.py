import chess
import chess.pgn as pgn
import chess.svg as svg

def save_svg(board, path):
	svg_text = svg.board(board, size=512)
	with open(path, 'w') as f:
			f.write(svg_text)

game = pgn.read_game(open("./data/1992-Fischer-Spassky.pgn", "r"))
board = game.board()
for move in game.mainline_moves():
	# Advance a turn
	board.push(move)
	break
save_svg(board, './data/1992-Fischer-Spassky.svg')


board = chess.Board(open("./data/8-queens-fundamental-1.txt", "r").read())
save_svg(board, './data/8-queens-fundamental-1.svg')