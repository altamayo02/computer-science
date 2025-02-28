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

def rank2(lst: list):
	ranked = [1]
	for i in range(1, len(lst)):
		j = len(ranked) - 1
		#print(f'j is {j}')
		#print(f'Is {lst[i]} < {lst[ranked[j] - 1]}?')
		while lst[i] < lst[ranked[j] - 1]:
			#print('Yes')
			j -= 1
			#print(f'Is {lst[i]} < {lst[ranked[j] - 1]}?')
			if j == -1:
				break
		#print('No')
		ranked.insert(j + 1, i + 1)
		#print(ranked)
	return ranked

def fundamentals(n: int) -> list:
	board = [i for i in range(1, n + 1)]
	sols = permute(board)

	funds = []
	done = []
	for s in sols:
		if s not in done:
			upper_s = [n - t + 1 for t in s]
			#s_rev = s[::-1]
			s_ranked = rank(s)
			#upper_s_rev = upper_s[::-1]
			# 1423 4132
			# 216354 561423
			upper_s_ranked = [n + 1 - t for t in s_ranked]
			for sol in [
				s,
				upper_s,
				#rank(s),
				s_ranked,
				#rank(upper_s),
				upper_s_ranked,
				#s_rev,
				s[::-1],
				#upper_s_rev,
				upper_s[::-1],
				#rank(s_rev),
				s_ranked[::-1],
				#rank(upper_s_rev)
				upper_s_ranked[::-1]
			]:
				done.append(sol)
			funds.append(s)
	
	return funds

print(len(fundamentals(8)))

#print(rank([2, 4, 3, 1]))
#print(rank2([2, 4, 3, 1]))

# 1:     1: 1
# 2:     1: 1
# 3:     2: 1
# 4:     7: 2
# 5:    23: 4
# 6:   115:
# 7:   694:
# 8:  5282:
# 9: 46066: