from graphviz import Digraph


ENGINES = [
	'dot',
	'neato',
	'fdp',
	'sfdp',
	'circo',
	'twopi',
	'osage',
	'patchwork'
]

class Automaton():
	def __init__(self, states: dict[str, dict[str, str]], start: str, ends: list[str], title) -> None:
		self.dot = Digraph(
			comment=title,
			format='png',
		)

		i = 0
		for state0 in states:
			shape = 'circle'
			if state0 in ends:
				shape = 'doublecircle'
			
			self.dot.node(
				state0,
				shape=shape
			)
			i += 1
		
		# To denote the start node
		self.dot.node('-BEGIN',	'Inicio', shape='plaintext', height='0', width='0')
		self.dot.edge('-BEGIN', start)

		for state0 in states:
			for state1 in states[state0]:
				self.dot.edge(state0, state1, states[state0][state1])
	
	def export(self, path):
		for engine in ENGINES:
			self.dot.render(
				filename=f'{path}/{engine}.gv',
				format='png',
				engine=engine,
				cleanup=True
			)

if __name__ == "__main__":
	seven = Automaton({
		'7': {
			'7.1': '3..5',
		},
		'7.1': {
			'7.2': '2..3'
		},
		'7.2': {
			'7.1': '4..6'
		}
	}, '7', ['7.2'], "7 queens")
	seven.export('./data/png/7-queens/')

	eight = Automaton({
		'8': {
			'8.1': '1..5',
		},
		'8.1': {
			'8': '2..6',
			'8.1.1': '2..5'
		},
		'8.1.1': {
			'8.1.2': '5..7'
		},
		'8.1.2': {
			'8.1.2': '2..5',
			'8.3': '2..6',
			'8.1.1': '2..8'
		},
		'8.2': {
			'8.2': '2..6, 3..7',
			'8.3': '2..7, 3..6',
			'8': '4..6'
		},
		'8.3': {
			'8.2': '2..7',
			'8.1.2': '4..8'
		}
	}, '8', ['8.1.1', '8.1.2', '8.2', '8.3'], "8 queens")
	eight.export('./data/png/8-queens/')