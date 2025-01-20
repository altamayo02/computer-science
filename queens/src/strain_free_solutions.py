def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    """Return the greatest common factor of two numbers."""
    while b:
        a, b = b, a % b
    return abs(a)

def factor(n):
    # Ensure the number is positive
    if n <= 0:
        return []

    factors = []
    # Loop through possible factors
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    
    return factors

def factor_primes(n):
	prime_factors = []

	if n == 0: return []
	elif n < 0:
		prime_factors.append(-1)
		n = -n

	# Check for factors from 2 to n
	for i in range(2, n + 1):
		while n % i == 0 and is_prime(i):
			prime_factors.append(i)
			n //= i
	
	return list(prime_factors)

def product(lst: list[int]):
    """Return the product of all items in the list."""
    product = 1
    for item in lst:
        product *= item
    return product

def strain_free_solutions(n):
	solutions = []
	for c1 in range(1, int(n / 2)):
		# det(M) = diag1 + (-diag2) = n
		# What we are trying to do here is finding all possible values for
		# diag1 and diag2, including their prime factors
		diag1 = n - c1
		ndiag2 = c1
		factors1 = factor_primes(diag1)
		factors2 = factor_primes(ndiag2)

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
				#i2, j1 = max(i2, j1), min(i2, j1)

				if (
					# Why does this work? Does it even work?
					# It might be that this prevents skewing,
					# as it prevents the system from starting at
					# a point higher than the first found vertically.
					j2 > i2 and
					# Queens threaten orthogonally, so
					# their coordinates cannot overlap
					# (cannot be equal or linearly dependent)
					gcd(i1, i2) == 1 and
					gcd(j1, j2) == 1 and
					# Queens threaten diagonally, so
					# the sum of their components must be coprime
					# (cannot be equal or linearly dependent)
					gcd(i1 - j1, i2 + j2) == 1 and
					gcd(i1 + j1, i2 - j2) == 1
				):
					if [i1, i2, j1, j2] not in solutions:
						solutions.append([i1, i2, j1, j2])
					if (
						# TODO - Only swap when swappable
						i1 != j2 and
						[i1, j1, i2, j2] not in solutions
					):
						solutions.append([i1, j1, i2, j2])
	return solutions

""" print(prime_factors(3628800))
print(prime_factors(3628800)[:5])
print(prime_factors(3628800)[5:])
print(prime_factors(9699690))
print(prime_factors(9699690)[:5])
print(prime_factors(9699690)[5:]) """

""" for n in range(0, 50):
	print(len(strain_free_solutions(n)), end=" ") """

for n in range(11, 12):
	print("%d:" % n)
	for sol in strain_free_solutions(n):
		print("\t%s" % sol)

"""
for n in range(1, 1000, 2):
	print("%d: %s" % (n, len(strain_free_solutions(n))))
"""

#print(factor_primes(986410))