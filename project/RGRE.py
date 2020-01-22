import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def rungame(players, turns, percentage):
	start_amount = 100
	array = setup(players, start_amount)

	for turn in range(1, turns+1):
		array = doturn(array, percentage)

		array = np.sort(array)

		if (turn-1)%50 == 0:
			# simple_graph(array, turn)
			# xbyy(array, turn, percentage)

			xownsy_graph(array, turn, percentage)
			# simple_graph(array, turn)

			# estimate_curve(array)

	# print(np.sum(array))

	# print(np.sum(array) - players*start_amount)
	# print(len(array[np.where(array < start_amount)])) 



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

def estimate_curve(array):
	x = np.arange(len(array))
	y = array

	# popt, _ = curve_fit(lambda t,a,b: a*np.exp(b*t),  x,  y)

	polyfit = np.polyfit(x, np.log(y), 2, w=np.sqrt(y))
	print(polyfit)
	polynomial = np.poly1d(polyfit)
	print(polynomial)
	plt.plot(x, polynomial(x), "-")


def simple_graph(array, turn):
	plt.loglog()
	plt.plot(array)
	plt.xlabel("Participant, sorted by least money first")
	plt.ylabel("Euro")
	plt.title(f"Amount of money per participant, time periods={turn}")

	plt.savefig(f"figures/simple/loglog/{turn}" + ".png")
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

	plt.loglog()
	# p_wealth_list = p_wealth_list[::-1]
	plt.bar(np.arange(bins), p_wealth_list)
	# plt.xticks(np.arange(bins), np.full(bins, f"{int(100/bins)}%"))
	plt.ylabel("Percentage of wealth")
	plt.title(f"Time periods={turn}, p={percentage}")


	# x = np.arange(bins)
	# y = p_wealth_list

	# polyfit = np.polyfit(x, np.log(y), 2, w=np.sqrt(y))
	# print(polyfit)
	# polynomial = np.poly1d(polyfit)
	# print(polynomial)
	# plt.plot(x, polynomial(x), "-")


	plt.savefig(f"figures/question3/loglog/{turn}" + ".png")
	plt.clf()


def xownsy_graph(array, turn, percentage):
	loglog = False

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


	# weights = np.ones((len(x)), dtype=int)
	# weights[0] = weights[0]*10
	# weights[-1] = weights[-1]*10
	# polyfit = np.polyfit(x, y, deg=2)
	# polynomial = np.poly1d(polyfit)
	# print(polynomial)


	# plt.plot(x, polynomial(x), "-")
	# print(polyfit)
	# formula = "y=%.4fx^2+(%.4fx)+(%.4f)" %(polyfit[0], polyfit[1], polyfit[2])
	# print(formula)

	if loglog:
		title_string = "Percentage of cumulative wealth owned by the participants \n loglog, p={p}, after {tp} periods"
		plt.title(title_string.format(p=percentage, tp=turn))

		plt.loglog()
		plt.savefig(f"figures/loglog/{turn}" + ".png")

	else:
		linear_line = np.linspace(0, 100, 100)

		title_string = "Percentage of cumulative wealth owned by the participants \n p={p}, after {tp} periods"
		plt.title(title_string.format(p=percentage, tp=turn))

		plt.plot(linear_line, linestyle="--", color="darkorange")
		plt.savefig(f"figures/normal/{turn}" + ".png")

	plt.clf()


rungame(10000, 2001, 5)