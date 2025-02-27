""" board1 = {
	{0, 1},
	{1, 2},
	{2, 0},
	{2, 0},
	{1, 2},
	{0, 1}
}

board2 = {
	{0, 2},
	{1, 0},
	{2, 1},
	{2, 1},
	{1, 0},
	{0, 2}
} """

def prime_factors(n):
	factors = []

	if n == 0: return []
	elif n < 0:
		factors.append(-1)
		n = -n

	# Check for number of 2s that divide n
	while n % 2 == 0:
		factors.append(2)
		n //= 2

	# n must be odd at this point, so we can skip even numbers
	for i in range(3, int(n**0.5) + 1, 2):
		while n % i == 0:
			factors.append(i)
			n //= i

	# This condition is to check if n is a prime number greater than 2
	if n > 2:
		factors.append(n)

	return factors

print(prime_factors(0))