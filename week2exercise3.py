import numpy as np

# spider trap avoidance factor
beta = 0.85
# all n connect bidirectional to each other n, and bidirectional to each p
number_n = 3
# all p connect bidirectional to each n, and directional from p to t
number_p = 1
# all f connect bidirectional to each t
number_f = 1

# DO NOT CHANGE BELOW
number_t = 1

# matrix rows and cols order: all n, then all p, then t, then all f
# example rows: n1 n2 n3 p1 p2 t f1 f2
# returns numpy matrix
def setup_matrix():

	# number of outgoing connections
	out_connections_n = number_n + number_p - 1
	out_connections_p = number_n + number_p
	out_connections_t = number_f
	out_connections_f = number_t

	# first node of type at index
	first_n = 0
	first_p = first_n + number_n
	first_t = first_p + number_p
	first_f = first_t + number_t
	total_size = first_f + number_f

	# ranges
	range_n = range(first_p)
	range_p = range(first_p, first_t)
	range_t = range(first_t, first_f)
	range_f = range(first_f, total_size)

	# probability of randomly taking each outgoing connection
	p_n = float(1)/out_connections_n
	p_p = float(1)/out_connections_p
	p_t = float(1)/out_connections_t
	p_f = float(1)/out_connections_f

	# make a numpy matrix of total_size by total_size
	# matrix = np.matrix(np.arange(total_size**2).reshape((total_size, total_size)))
	matrix = np.zeros((total_size, total_size))
	matrix = np.matrix(matrix)

	for x in range(total_size):
		if x in range_n:
			# all n go to all n
			for y in range_n:
				if x != y:
					matrix.put((y*total_size + x), p_n)
			# all n go to all p
			for y in range_p:
				matrix.put((y*total_size + x), p_n)

		elif x in range_p:
			# all p go to all p
			for y in range_p:
				if x != y:
					matrix.put((y*total_size + x), p_p)
			# all p go to all n
			for y in range_n:
				matrix.put((y*total_size + x), p_p)

		elif x in range_t:
			# all t go to f
			for y in range_f:
				matrix.put((y*total_size + x), p_t)

		elif x in range_f:
			# all f to to all t
			for y in range_t:
				matrix.put((y*total_size + x), p_f)

	return matrix

def converge(matrix, beta, vertex=None):

	matrix_size = len(matrix)
	empty_vertex = np.arange(matrix_size, dtype=float)
	scalar_beta = np.full_like(empty_vertex, beta)
	scalar_rest = np.full_like(empty_vertex, 1-beta)
	try:
		vertex.any()
	except:
		vertex = np.full_like(empty_vertex, 1/matrix_size)

	first = np.dot(matrix, vertex)
	first = np.multiply(scalar_beta, first)
	second = np.multiply(scalar_rest, vertex)

	result = np.add(first, second)

	return result

def run_test():
	test_matrix = np.matrix([[0, 1/2, 0, 0], 
						[1/3, 0, 0, 1/2], 
						[1/3, 0, 1, 1/2], 
						[1/3, 1/2, 0, 0]])
	result = converge(test_matrix, beta).getA1()
	old_result = None
	print("first calculation: ", result)
	while not np.array_equal(result, old_result):
		old_result = result
		result = converge(test_matrix, beta, old_result).getA1()

	return result

def run_program():
	matrix = setup_matrix()
	result = converge(matrix, beta).getA1()
	old_result = None
	while not np.array_equal(result, old_result):
		old_result = result
		result = converge(matrix, beta, old_result).getA1()


print("converged result: ", run_test())