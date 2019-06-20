import random

import math, wave
import numpy as np
import matplotlib.pyplot as plt


def test1():

	path = "./music/in_game_music_1.wav"

	wr = wave.open(path, 'r')

	fr = 10
	sz = wr.getframerate() // fr  # Read and process 1/fr second at a time.
	# A larger number for fr means less reverb.
	c = int(wr.getnframes() / sz)  # count of the whole file

	for num in range(c):
		da = np.fromstring(wr.readframes(sz), dtype=np.int16)
		left, right = da[0::2], da[1::2]  # left and right channel
		# lf, rf = np.fft.rfftfreq(left), np.fft.rfftfreq(right)

		a = left
		# a = np.fft.fft(left)
		b = np.fft.rfft(left)



		fig, ax1 = plt.subplots()

		ax1.plot(range(len(a)), a, color='m')
		# ax1.plot(range(len(b)), b, color='g')

		ax2 = ax1.twinx()
		ax2.plot(range(len(b)), b, color='g')

		fig.legend(['w', 'f'])
		fig.tight_layout()
		fig.show()

def gen_wave(frequency, length, sample_rate):
	return np.array([math.cos(math.pi * 2 * frequency * i / sample_rate) for i in range(sample_rate * length)])

def get_mix(t):
	sample_rate = 2000
	length = 1

	total = 0
	for n in t:
		total += gen_wave(n, length, sample_rate)
	total /= len(t)

	return total

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def test2():
	# maxf = 1000
	# frequencys = [random.uniform(0, maxf) for _i in range(3)]
	# # frequencys = [i for i in range(20, 30)]
	# sample = get_mix(frequencys)
	#
	# if 1:

	path = "./audio/toto_africa.wav"
	music = wave.open(path, 'r')


	frame_rate = 10
	sample_size = music.getframerate() // frame_rate  # Read and process 1/fr second at a time.
	# A larger number for fr means less reverb.
	number_of_slices = int(music.getnframes() / sample_size)  # count of the whole file

	for _slice_number in range(number_of_slices):
		da = np.fromstring(music.readframes(sample_size), dtype=np.int16)
		left, right = da[0::2], da[1::2]  # left and right channel
		# lf, rf = np.fft.rfftfreq(left), np.fft.rfftfreq(right)

		sample = left
		# sample /= 1500

		graph = np.abs(np.fft.rfft(sample).real)
		graph1 = sigmoid(graph) * 2 - 1


		sum = 0
		i = 0
		for n in graph1:
			sum += i * n
			i += 1
		avg = 1 - (sum / i)
		print(avg)

		# min = 20
		# max = 20000
		# m2m = max - min  # min to max
		#
		# x = []
		# y = []
		# for i in range(m2m):
		# 	freq = freqs[min + i]
		# 	theta = (i/m2m) * (5/6)  # *5/6 cuts pink from the rainbow
		# 	x += [freq * math.sin(theta)]
		# 	y += [freq * math.cos(theta)]
		# x = sum(x)/m2m
		# y = sum(x)/m2m


		# min = 100
		# max = 1000

		min = 0
		max = len(graph1)

		l = max - min

		graph1 = graph1[min:max]

		points_x = []
		points_y = []
		for i in range(l):
			freq = graph1[i]
			theta = i / l
			theta *= (5/6)  # *5/6 cuts pink from the rainbow
			theta *= math.pi * 2
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]
		# freqs = np.fft.fftfreq(len(graph1))

		x = np.sum(points_x) / len(points_x)
		y = np.sum(points_y) / len(points_y)
		z = math.sqrt(x*x + y*y)
		print(x, y, z)


		fig, ax1 = plt.subplots()
		ax1.plot(range(len(graph)), graph, color='b')
		fig.show()

		fig, ax2 = plt.subplots()
		ax2.plot(range(len(graph1)), graph1, color='b')
		fig.show()

		fig, ax3 = plt.subplots()
		ax3.plot(points_x, points_y, color='b')
		fig.show()

		# ax2 = ax1.twinx()
		fig, ax2 = plt.subplots()
		ax2.plot(range(len(sample)), sample, color='g')
		# ax2.plot(range(len(freqs)), freqs, color='b')
		fig.show()


		# fig.legend(['1', '2', '3'])
		# fig.tight_layout()
		# fig.show()

		print("moo")


if __name__ == "__main__":
	test2()
