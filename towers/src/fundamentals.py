# lanas,
from itertools import permutations
from copy import deepcopy

def permute(lst: list):
	perms = permutations(lst)
	perms = [list(perm) for perm in perms]
	return perms

def rank(lst: list):
	opposite = [(v, k) for k, v in enumerate(lst)]
	ranked = sorted(opposite, key=lambda r: r[0])
	ranked = [r[1] + 1 for r in ranked]
	return ranked

def fundamentals(n: int) -> list:
	board = [i for i in range(1, n + 1)]
	sols = permute(board)

	funds = []
	for s in sols:
		upper_s = [n - t + 1 for t in s]
		if all(rep not in funds for rep in [s, upper_s, rank(s), rank(upper_s)]):
			funds.append(s)
	
	return funds

print(fundamentals(3))