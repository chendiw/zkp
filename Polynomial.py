import copy

class Polynomial:
	def __init__(self, num_var, degrees, coefficients):
		self.num_var = num_var
		self.degrees = degrees
		self.coefficients = coefficients

	# var_values = {0: 0, 2:3} --- 1 as first variable,  2 as third variable
	def __call__(self, var_values):
		new_coefficients = copy.deepcopy(self.coefficients)
		new_degrees = copy.deepcopy(self.degrees)
		count = 0
		# self.var_remain = [True] * self.num_var
		for key in var_values.keys():
			var_index = key
			# self.var_remain[var_index] = False
			value = var_values[key]
			for i in range(len(self.coefficients)):
				new_coefficients[i] = new_coefficients[i] * value**self.degrees[i][var_index]
				new_degrees[i].pop(var_index - count)
			count += 1
		remaining_var = self.num_var - len(var_values.keys())
		if remaining_var != 0:
			return Polynomial(remaining_var, new_degrees, new_coefficients)
		else:
			return sum(new_coefficients)

	def get_degrees(self):
		return self.degrees

	def get_coefficients(self):
		return self.coefficients

