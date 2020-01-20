import numpy as np
import matplotlib.pyplot as plt

def rungame(players, turns, percentage):
	start_amount = 100
	array = setup(players, start_amount)

	for turn in range(turns):
		array = doturn(array, percentage)

	array = np.sort(array)
	# array = array[::-1]

	# simple_graph(array)
	xownsy_graph(array)

	print(np.sum(array))

	print(np.sum(array) - players*start_amount)
	print(len(array[np.where(array < start_amount)])) 



def setup(players, start_amount):
	array = np.full(players, start_amount)
	return array

def doturn(array, percentage):
	np.random.shuffle(array)

	arrays = np.array_split(array, 2)
	f_array = arrays[0]
	l_array = arrays[1]

	f_array = f_array*(1+percentage/100)
	l_array = l_array*(1-percentage/100)

	array = np.concatenate((f_array, l_array))

	return array

def simple_graph(array):
	# plt.loglog()
	plt.plot(array)
	plt.show()

def xownsy_graph(array):
	# plt.hist(array, 10, density=100)
	# plt.show()

	total = np.sum(array)
	length = len(array)
	bins = 20
	binsize = int(length/bins)

	p_percent_list = []
	m_percent_list = []

	for i in range(0, bins+1):
		last_index = binsize*i
		indices = list(range(0, last_index))
		summed = array[indices].sum()
		m_percentage = int(summed/total*100)
		p_percentage = int(i*(100/bins))

		m_percent_list.append(m_percentage)
		p_percent_list.append(p_percentage)

	plt.scatter(p_percent_list, m_percent_list)

	plt.xlabel("Percentage of participants")
	plt.ylabel("Percentage of wealth (cumulative)")

	linear_line = np.linspace(0, 100, 100)

	plt.plot(linear_line, color="darkorange")
	# plt.loglog()
	plt.show()


rungame(10000, 100, 10)