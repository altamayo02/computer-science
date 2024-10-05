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

def factorize(n):
    # Ensure the number is positive
    if n <= 0:
        return []

    factors = []
    # Loop through possible factors
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    
    return factors

def factorize_primes(n):
    # Ensure the number is positive
    if n <= 0:
        return []

    prime_factors = []
    # Check for factors from 2 to n
    for i in range(2, n + 1):
        while n % i == 0 and is_prime(i):
            prime_factors.append(i)
            n //= i
            
    return list(prime_factors)  # Return every prime factor

def product(lst: list[int]):
    """Return the product of all items in the list."""
    product = 1
    for item in lst:
        product *= item
    return product

def strain_free_solutions(n):
	solutions = []
	for counter1 in range(1, n):
		diag1 = n - counter1
		diag2 = counter1
		
		factors1 = factorize_primes(diag1)
		factors2 = factorize_primes(diag2)
		while len(factors2) < 2:
			factors2.append(1)
		# Constructing i and j
		for counter2 in range(1, len(factors1)):
			for counter3 in range(1, len(factors2)):
				i1 = product(factors1[:counter2])
				j2 = product(factors1[counter2:])
				i2 = product(factors2[:counter3])
				j1 = product(factors2[counter3:])
				i1, j2 = max(i1, j2), min(i1, j2)
				i2, j1 = max(i2, j1), min(i2, j1)
				# If components are in the right order (i1 >= j2 > i2 >= j1)
				# and (i + j)'s components are coprime
				if (
					j2 > i2 and
					gcd(i1, i2) == 1 and
					gcd(j1, j2) == 1 and
					gcd(i1 - j1, i2 + j2) == 1 and
					gcd(i1 + j1, i2 - j2) == 1
				):
					if [i1, j2, i2, j1] not in solutions:
						solutions.append([i1, j2, i2, j1])
				#print(diag1, diag2, factors1, factors2, [i1, j2, i2, j1])
	return solutions


for n in range(1, 71):
	print("%d:" % n)
	for sol in strain_free_solutions(n):
		print("\t%s" % sol)

"""
for n in range(1, 1000, 2):
	print("%d: %s" % (n, len(strain_free_solutions(n))))
"""