from services.json_service import JsonService

def gcd(a, b):
	"""Return the greatest common factor of two numbers."""
	while b:
		a, b = b, a % b
	return abs(a)

def is_prime(n):
	"""Check if a number is prime."""
	if n <= 1: return False
	if n <= 3: return True
	if n % 2 == 0 or n % 3 == 0: return False

	i = 5
	# Check for factors up to sqrt(n)
	while i ** 2 <= n:
		if n % i == 0 or n % (i + 2) == 0:
			return False
		# Check numbers of the form 6k +- 1
		i += 6
	
	return True

def factor_primes(n):
	"""Return the factors of a number."""
	prime_factors = []

	if n == 0: return []
	elif n < 0:
		prime_factors.append(-1)
		n = -n

	primes = gen_primes(n)
	# Check for factors from 2 to n
	for p in primes:
		if n % p == 0:
			prime_factors.append(p)
	
	return list(prime_factors)

def product(lst: list[int]):
		"""Return the product of all items in the list."""
		product = 1
		for item in lst:
				product *= item
		return product

def perfect_solutions(n):
	if n < 4: return []
	solutions = []
	if n % 2 == 0 or n % 3 == 0: return solutions

	primes = gen_primes(n)
	print(primes)
	# After first half: Same combination, different orientation
	# (We care about the combination, not the permutation)
	for c1 in range(1, int(n / 2) + 1):
		# det(M) = diag1 + (-diag2) = n
		# What we are trying to do here is finding all possible values for
		# diag1 and diag2, including their prime factors.
		# diag2 is implied negative
		diag1 = n - c1
		# i1 will be prime and j2 will be 1, but 0 < j1 < j2
		if diag1 in primes: continue
		diag2 = c1
		factors1 = factor_primes(diag1)
		print(factors1)
		factors2 = factor_primes(diag2)

		# Pad with ones if needed
		while len(factors2) < 2:
			factors2.append(1)
		
		# Construct i and j
		for c2 in range(1, len(factors1)):
			for c3 in range(1, len(factors2)):
				# Partition prime factors into two numbers
				# to fit the primary diagonal
				i1 = product(factors1[c2:])
				j2 = product(factors1[:c2])
				# Partition prime factors into two numbers
				# to fit the secondary diagonal
				i2 = product(factors2[:c3])
				j1 = product(factors2[c3:])

				# Since i1j2 + i2j1 = n
				# and multiplication is commutative
				# we use the convention that i1 >= j2
				i1, j2 = max(i1, j2), min(i1, j2)
				# i2 and j1 CAN be swapped for a new solution
				# (in the case they aren't equal)
				i2, j1 = max(i2, j1), min(i2, j1)

				if (
					# Queens threaten orthogonally, so
					# their coordinates cannot overlap
					# (cannot be equal or linearly dependent)
					# Also, if i2 is bigger than j2, it means there is an ignored point
					# under i2, which means the solution is skewed. Same for i1 < j1
					i1 <= j1 or i2 >= j2 or
					
					# Queens threaten diagonally, so for diagonals
					# the components of i and j each must be coprime
					# (cannot be equal or linearly dependent)
					i1 <= i2 or j1 >= j2 or
					gcd(i1, i2) != 1 or gcd(j1, j2) != 1 or
					# The sum of their components must be coprime too
					gcd(i1 - j1, i2 + j2) != 1 or gcd(i1 + j1, i2 - j2) != 1
				): continue

				if [i1, i2, j1, j2] not in solutions:
					solutions.append([i1, i2, j1, j2])
				
				# Only swap i2 and j1 when swappable
				if i1 != j2 and i2 != j1:
					solutions.append([i1, j1, i2, j2])
	return solutions

def gen_perfect_composites(limit):
	composites = []
	primes = gen_primes(limit)
	for n in range(0, limit):
		#print(f'{n}...')
		if n not in primes:
			sols = perfect_solutions(n)
			print(n)
			print(sols)
			if len(sols) != 0: composites.append(n)
		#print('\u001b[;H')
	#print(composites)

	composite_factors = { c: {} for c in composites }
	for c in composites:
		#print("%4d" % c, end=' ')
		factors = factor_primes(c)

		for f in factors:
			if f not in composite_factors[c]:
				composite_factors[c][f] = 1
			else:
				composite_factors[c][f] += 1
	
	json = JsonService()
	json.save_json(f'./queens/data/json/{limit}_perfect_composite_factors.json', composite_factors)

############## Testing

def primes_table(k, l):
	# k = 1000
	# l = 40
	for i in range(0, int(k / 40)):
		# Header values (0 to 25 * 40)
		x = '\u001b[96m'
		y = ''
		for n in range(l * i, l * (i + 1)):
			x += "%3d " % n

			solutions = perfect_solutions(n)
			if len(solutions) == 0:
				y += '\u001b[91m'
			else:
				y += "\u001b[93m"	if is_prime(n) else	'\u001b[103m'
			
			y += "%3d\u001b[0m " % len(solutions)
		print(x)
		print(y)

def gen_primes(limit):
	if limit <= 1: return []
	elif limit == 2: return [2]

	primes = [2, 3]
	test_num = 5
	while test_num <= limit:
		is_prime = True
		for p in primes:
			if test_num % p == 0:
				is_prime = False
				break
		if is_prime:
			primes.append(test_num)
		test_num += 2
	return primes

print(perfect_solutions(5))

""" for n in range(1, 100, 2):
	print("%d:" % n)
	for sol in perfect_solutions(n):
		print("\t%s" % sol) """

""" for n in range(1, 100, 2):
	print("%d: \n\t%s" % (n, len(perfect_solutions(n)))) """