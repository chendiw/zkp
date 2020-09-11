from Polynomial import Polynomial

# GKR protocol with random linear combinations
# Prover runtime: O(|C|log|C|)
# Verifier runtime: O(n+k+dlog|C|+T), T = polylog|C|

# Generate an array of length-array of binaries
def generate_binaries(lst, length):
	while len(lst[0]) < length:
		num = len(lst)
		for i in range(num):
			arr = lst[i]
			arr1 = copy.deepcopy(arr)
			arr.append(0)
			arr1.append(1)
			lst.append(arr1)
	return np.array(lst)

def binary_arr_to_number(bi_array):
	return int("".join(bi_array.astype(str)), 2)

def binary_arr_to_str(bi_array):
	return "".join(bi_array.astype(str))

# g=g_1, ... g_l (index 0 as dummy element) (length of g_list = l+1)
# O(2**l)
def precompute(g_list):
	G = [0] * (2 ** (len(g_list) - 1))
	G[0] = 1
	for i in range(l):
		b_list = generate_binaries([[0], [1]], i)
		for b in b_list:
			b_number = binary_arr_to_number(b)
			G[b_number * 2] = G[b_number] * (1 - g_list[i+1])
			G[b_number * 2 + 1] = G[b_number] * g_list[i+1]
	return G

# TBD: Answer to Question 4
def nonzero_arg_search(f_1):
	# List of (z, x, y)
	nonzero_args = []
	return nonzero_args

# A_f2 and A_f3 both initialized to be evaluations on a hypercube
# Question 2: What are evaluations on a hypercube? (Something like f(x) where x is a length-n bit string?)
def initialize_phase_one(f_1, f_3, A_f3, g_list):
	G = precompute(g_list)
	x_list = generate_binaries([[0], [1]], len(g_list)-1)
	A_hg = [0] * (2 ** (len(g_list) - 1))
	# Question 3: How to efficiently search for all (z, x, y) s.t. f_1(z, x, y)!=0 (How to utilize the fact that f_1 is sparse?)
	nonzero_args = nonzero_arg_search(f_1)
	for z, x, y in nonzero_args:
		x_number = binary_arr_to_number(x)
		z_number = binary_arr_to_number(z)
		y_number = binary_arr_to_number(y)
		# Question 4: How to compute f_1(z, x, y)? Why in GKR f_1(z, x, y)=1?
		A_hg[x_number] = A_hg[x_number] + G[z_number] * f_1(z, x, y) * A_f3[y_number]
	return A_hg

# g_list = 0, g_1, ... g_l, u_list = 0, u_1, ... u_l
def initialize_phase_two(f_1, g_list, u_list):
	G = precompute(g_list)
	U = precompute(u_list)
	y_list = generate_binaries([[0], [1]], len(g_list)-1)
	A_f1 = [0] * (2 ** (len(g_list) - 1))
	nonzero_args = nonzero_arg_search(f_1)
	for z, x, y in nonzero_args:
		x_number = binary_arr_to_number(x)
		z_number = binary_arr_to_number(z)
		y_number = binary_arr_to_number(y)
		A_f1[y_number] = A_f1[y_number] + G[z_number] * U[x_number] * f_1(z, x, y)
	return A_f1

# Function evaluations
# r_list has a dummy value at index 0
def function_evaluations(f, A, r_list):
	F = {}
	num_variables = len(r_list) - 1
	for i in range(1, num_variables+1):
		b_list = generate_binaries([[0], [1]], num_variables - i)
		for b in b_list:
			for t in [0, 1, 2]: # Question 1: why t = 2?
				# f(r_list[:(i-1)], t, b) = A[b] * (1 - t) + A[b + 2**(l-i)] * t
				b_number = binary_arr_to_number(b)
				F[str(t)+binary_arr_to_str(b)] = A[b_number] * (1 - t) + A[b_number + 2**(l-i)] * t
			A[b_number] = A[b_number] * (1 - r_list[i]) + A[b_number + 2**(l-i)] * r_list[i] 
	return F

# SumCheck
def sum_check(f, A, r_list):
	a_list = []
	F = function_evaluations(f, A, r_list)
	num_variables = len(r_list) - 1
	for i in range(1, num_variables+1):
		a_i = []
		b_list = generate_binaries([[0], [1]], num_variables - i)
		for t in [0, 1, 2]:
			a_i[t] = sum(F[str(t)+binary_arr_to_str(b)] for b in b_list)
		a_list.append(a_i)
	return a_list

# SumCheckProduct  
def sum_check_product(f, A_f, g, A_g, r_list):
	a_list = []
	F = function_evaluations(f, A_f, r_list)
	G = function_evaluations(g, A_g, r_list)
	for i in range(len(r_list)):
		a_i = []
		b_list = generate_binaries([[0], [1]], num_variables - i)
		for t in [0, 1, 2]:
			a_i[t] = sum(F[str(t)+binary_arr_to_str(b)]*G[str(t)+binary_arr_to_str(b)] for b in b_list)
	return a_list

# Global variable A_f3, A_f2
def sum_check_gkr(f_1, f_2, f_3, u_list, v_list, g_list):
	A_hg = initialize_phase_one(f_1, f_3, A_f3, g_list)
	# TBD: h_g(x)
	a_list_first = sum_check_product(A_hg, f_2, A_f2, u_list)
	A_f1 = initialize_phase_two(f_1, g_list, u_list)
	a_list_second = sum_check_product(f_1(g, u, y), A_f1, f_3(y)*f_2(u), A_f3*f_2(u), v_list)
	return a_list_first + a_list_second

if __name__ == "__main__":

	NUM_VARIABLES = 3
	DEGREES = [[1, 2, 1], [2, 3, 1], [0, 1, 0], [0, 0, 0]]
	COEFFICIENTS = [2, 3, -1, -4]
	f_1 = Polynomial(num_var, degrees, coefficients)


