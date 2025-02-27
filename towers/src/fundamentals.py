# lanas,
from itertools import permutations
from copy import deepcopy

def permute(lst: list):
	perms = permutations(lst)
	perms = [list(perm) for perm in perms]
	return perms

def rank(lst: list):
	# TODO - Implement iteratively, appending either left or right
	# for less than and greater than
	opposite = [(v, k) for k, v in enumerate(lst)]
	ranked = sorted(opposite, key=lambda r: r[0])
	ranked = [r[1] + 1 for r in ranked]
	return ranked

def fundamentals(n: int) -> list:
	board = [i for i in range(1, n + 1)]
	sols = permute(board)

	funds = []
	done = []
	for s in sols:
		if s not in done:
			upper_s = [n - t + 1 for t in s]
			s_rev = s[::-1]
			upper_s_rev = upper_s[::-1]
			# TODO - Rank less, reverse more
			# 1423 4132
			# 216354 561423
			for sol in [
				s,
				upper_s,
				rank(s),
				rank(upper_s),
				s_rev,
				upper_s_rev,
				rank(s_rev),
				rank(upper_s_rev)
			]:
				done.append(sol)
			funds.append(s)
	
	return funds

print(len(fundamentals(9)))

# 1:     1: 1
# 2:     1: 1
# 3:     2: 1
# 4:     7: 2
# 5:    23: 4
# 6:   115:
# 7:   694:
# 8:  5282:
# 9: 46066: