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
	return np.array([math.cos(math.tau * frequency * i / sample_rate) for i in range(sample_rate * length)])

def test2():
	sample_rate = 100
	length = 2
	points = length * sample_rate

	wave1 = gen_wave(1, length, sample_rate)
	wave2 = gen_wave(3, length, sample_rate)
	wave3 = (wave1 + wave2) / 2

	graph1 = np.fft.rfft(wave1) / sample_rate

	fig, ax1 = plt.subplots()

	ax1.plot(range(points), wave1, color='b')
	# ax1.plot(range(points), wave2, color='g')
	# ax1.plot(range(points), wave3, color='b')

	ax2 = ax1.twinx()
	ax2.plot(range(len(graph1)), graph1, color='g')

	fig.legend(['1', '2', '3'])
	fig.tight_layout()
	fig.show()

	print("moo")


if __name__ == "__main__":
	test2()
