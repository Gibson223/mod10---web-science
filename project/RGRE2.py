import numpy as np
import matplotlib.pyplot as plt
import random as random

def rungame(players, turns, percentage):
	start_amount = 100
	array = setup(players, start_amount)

	for turn in range(1, turns+1):

		array = doturn(array, percentage)
		array = np.sort(array)

		if (turn-1)%100 == 0:
			simple_graph(array, turn)
			xbyy(array, turn, percentage)
			xownsy_graph(array, turn, percentage)


def setup(players, start_amount):
	array = np.full(players, start_amount)
	return array

def doturn(array, percentage):
	new_array = []

	for item in array:
		random_int = random.randint(1, 4)
		multiplier = 1
		if random_int > 2:
			if random_int == 3:
				multiplier = 1.05
			else:
				multiplier = 1.10
		else:
			if random_int == 1:
				multiplier = 0.9
			else:
				multiplier = 0.95
		new_array.append(item*multiplier)

	array = np.array(new_array)

	return array


def simple_graph(array, turn):
	plt.plot(array)
	plt.xlabel("Participant, sorted by least money first")
	plt.ylabel("Euro")
	plt.title(f"Amount of money per participant, time periods={turn}")

	plt.savefig(f"figures/model2/simple/{turn}" + ".png")

	plt.loglog()
	plt.savefig(f"figures/model2/simple/loglog/{turn}" + ".png")
	plt.clf()

def xbyy(array, turn, percentage):
	total = np.sum(array)
	bins = 20
	binsize = int(len(array)/bins)

	p_wealth_list = []

	for i in range(1, bins+1):
		first_index = binsize*(i-1)
		last_index = binsize*i
		indices = list(range(first_index, last_index))
		summed = array[indices].sum()

		p_wealth_list.append(summed/total*100)

	# p_wealth_list = p_wealth_list[::-1]
	plt.bar(np.arange(bins), p_wealth_list)
	plt.xticks(np.arange(bins), np.full(bins, f"{int(100/bins)}%"))
	plt.ylabel("Percentage of wealth")
	plt.title(f"Time periods={turn}, p={percentage}")


	# x = np.arange(bins)
	# y = p_wealth_list

	# polyfit = np.polyfit(x, np.log(y), 2, w=np.sqrt(y))
	# print(polyfit)
	# polynomial = np.poly1d(polyfit)
	# print(polynomial)
	# plt.plot(x, polynomial(x), "-")


	plt.savefig(f"figures/model2/xbyy/{turn}" + ".png")

	plt.loglog()
	plt.xticks(None)
	plt.savefig(f"figures/model2/xbyy/loglog/{turn}" + ".png")
	plt.clf()


def xownsy_graph(array, turn, percentage):

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

	# plt.plot(p_percent_list, m_percent_list, 'o')

	plt.xlabel("Percentage of participants")
	plt.ylabel("Percentage of wealth (cumulative)")

	x = p_percent_list
	y = m_percent_list
	plt.plot(x, y, 'o')

	title_string = "Percentage of cumulative wealth owned by the participants \n loglog, p={p}, after {tp} periods"
	plt.title(title_string.format(p=percentage, tp=turn))
	plt.loglog()
	plt.savefig(f"figures/model2/xownsy/loglog/{turn}" + ".png")



	linear_line = np.linspace(0, 100, 100)
	title_string = "Percentage of cumulative wealth owned by the participants \n p={p}, after {tp} periods"
	plt.title(title_string.format(p=percentage, tp=turn))
	plt.plot(linear_line, linestyle="--", color="darkorange")
	plt.xscale('linear')
	plt.yscale('linear')
	plt.savefig(f"figures/model2/xownsy/{turn}" + ".png")

	plt.clf()


rungame(10000, 1001, 5)