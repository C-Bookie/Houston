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
	sample_rate = 100
	length = 4

	total = 0
	for n in t:
		total += gen_wave(n, length, sample_rate)
	total /= len(t)

	return np.fft.rfft(total) / sample_rate


def test2():
	max = 20
	graph1 = get_mix([random.uniform(0, max) for i in range(100)])

	if 1:

	# path = "./music/in_game_music_1.wav"
	# wr = wave.open(path, 'r')
	#
	#
	# fr = 10
	# sz = wr.getframerate() // fr  # Read and process 1/fr second at a time.
	# # A larger number for fr means less reverb.
	# c = int(wr.getnframes() / sz)  # count of the whole file
	#
	# for num in range(c):
	# 	da = np.fromstring(wr.readframes(sz), dtype=np.int16)
	# 	left, right = da[0::2], da[1::2]  # left and right channel
	# 	# lf, rf = np.fft.rfftfreq(left), np.fft.rfftfreq(right)
	#
	# 	graph1 = np.fft.rfft(left)

		graph1 += 1
		graph1 /= 2

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


		min = 0
		max = len(graph1)
		l = max - min

		points_x = []
		points_y = []
		for i in range(min, max):
			freq = graph1[min + i]
			theta = math.pi * (i/l) * (5/6)  # *5/6 cuts pink from the rainbow
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]
		freqs = np.fft.fftfreq(len(graph1), graph1)

		x = 0
		for point in points_x:
			x += point

		y = 0
		for point in points_y:
			y += point

		# z = math.sqrt(x*x + y*y)
		#
		# print(x, y, z)

		fig, ax1 = plt.subplots()

		# ax1.plot(range(points), wave1, color='b')
		# ax1.plot(range(points), wave2, color='g')
		# ax1.plot(range(points), wave3, color='b')
		# ax1.plot(points_x, points_y, color='b')
		ax1.plot(range(len(freqs)), freqs, color='b')

		ax2 = ax1.twinx()
		ax2.plot(range(len(graph1)), graph1, color='g')


		fig.legend(['1', '2', '3'])
		fig.tight_layout()
		fig.show()

	print("moo")


if __name__ == "__main__":
	test2()
