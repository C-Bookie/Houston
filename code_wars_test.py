
def get_number_of_value_crossings(signal, value):
	if len(signal) < 2:
		return 0

	sum = 0
	side = False
	first = value == signal[0]
	for n in signal:
		if first:
			if value != n:
				first = False
				side = value < n
		elif n < value if side else value < n:
			sum += 1
			side = not side
	return sum

def test():
	print("test started")
	thresh_val = 2
	list_ = [1,2,3,2,3,2,1]
	# general condition.
	assert get_number_of_value_crossings(list_, thresh_val) == 2, "this should cross twice"
	list_ = [2,2,1]
	# condition of starting on the then going negative.
	assert get_number_of_value_crossings(list_, thresh_val) == 0, "this should never change side"
	list_ = [2,2,3]
	# condition of starting on the then going positive.
	assert get_number_of_value_crossings(list_, thresh_val) == 0, "this should never change side"
	list_ = []
	# empty condition
	assert get_number_of_value_crossings(list_, thresh_val) == 0, "this should never change side"
	print("test done")


if __name__ == '__main__':
	test()
