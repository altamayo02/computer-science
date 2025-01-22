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
	# After first half: Same combination, different orientation
	# (We care about the combination, not the permutation)
	for c1 in range(1, int(n / 2) + 1):
		# det(M) = diag1 + (-diag2) = n
		# What we are trying to do here is finding all possible values for
		# diag1 and diag2, including their prime factors.
		# diag2 is implied negative
		diag1 = n - c1
		# i1 will be prime and j2 will be 1, but 0 < j1 < j2
		if is_prime(diag1): continue
		diag2 = c1
		factors1 = factor_primes(diag1)
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
					gcd(i1, i2) != 1 or gcd(j1, j2) != 1
				): continue

				if (
					# The sum of their components must be coprime too
					# But... will these diagonals ever be able to align?
					gcd(i1 - j1, i2 + j2) != 1 or gcd(i1 + j1, i2 - j2) != 1
				):
					print(f"\t%2d, %2d: %s" % (
						gcd(i1 - j1, i2 + j2), gcd(i1 + j1, i2 - j2), [i1, i2, j1, j2]
					))

				if [i1, i2, j1, j2] not in solutions:
					solutions.append([i1, i2, j1, j2])
				
				# Only swap when swappable
				if i1 != j2 and i2 != j1:
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

""" for n in range(13, 14):
	print("%d:" % n)
	for sol in strain_free_solutions(n):
		print("\t%s" % sol) """

for n in range(1, 100, 2):
	#print("%d: \n\t%s" % (n, len(strain_free_solutions(n))))
	print(f"{n}:")
	strain_free_solutions(n)


#print(factor_primes(986410))