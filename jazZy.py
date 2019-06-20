#testing phue and mqtt for motion sensing lights
import threading
import wave

import math
import phue
import time
import random
import json

import pyaudio as pyaudio
import pygame

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import pychorus
from pychorus import similarity_matrix

deadzone = 0.25

def correctJoy(n):
	if n < deadzone and n > -deadzone:
		return 0.
	if n < 0:
		return -n**2
	return n**2

def run():
	b = phue.Bridge('192.168.1.211')
	b.connect()
	print(b.get_api())

	pygame.init()
	# surface = pygame.display.set_mode((400, 300), 0, 32)

	pygame.joystick.init()
	joysticks = []
	for i in range(pygame.joystick.get_count()):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
		print("Initialised: ", joystick.get_name())
		joysticks += [joystick]

	# light_names = b.get_light_objects('name')
	# light_names['cal'].colormode = 'hs'

	speed = 1

	base = 0
	last = 0
	offset = 0
	button_hot = [False] * joysticks[0].get_numbuttons()

	recorded = []
	replay = False


	count = 0
	while True:
		pygame.event.pump()

		temp = {
			"axis": [joysticks[0].get_axis(i) for i in range(joysticks[0].get_numaxes())],
			"balls": [joysticks[0].get_ball(i) for i in range(joysticks[0].get_numballs())],
			"buttons": [joysticks[0].get_button(i) for i in range(joysticks[0].get_numbuttons())],
			"hats": [joysticks[0].get_hat(i) for i in range(joysticks[0].get_numhats())],
		}

		if replay:
			temp["axis"] = recorded[count % len(recorded)]

		for i in range(joysticks[0].get_numbuttons()):
			if temp["buttons"][i]:
				if not button_hot[i]:
					button_hot[i] = True
					if i == 0:
						base = random.uniform(0, 1)
					if i == 1:
						last = (((1+temp["axis"][0]) / 2)+offset) % 1
					if i == 4:
						if len(recorded) > 0:
							replay = not replay
					if i == 2:
						recorded = []
						replay = False
			else:

				if button_hot[i]:
					button_hot[i] = False

		if button_hot[2]:
			recorded += [temp["axis"]]

		if button_hot[1]:
			offset = (last-((1+temp["axis"][0]) / 2)) % 1

		command = {
			'transitiontime': int(speed*10),
			'bri': int((1-((1+temp["axis"][3]) / 2)) * 254),
			'hue': int(((base+(((1+temp["axis"][0]) / 2)+offset)) % 1) * 65535),
			'sat': int((1-((1+temp["axis"][1]) / 2)) * 254)
		}

		print(count)
		print(temp)
		print(command)
		b.set_light('cal', command)

		time.sleep(speed)
		count += 1


class MusicPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)
		s.f = wave.open(path, 'r')
		s.chunk = 1024
		s.p = pyaudio.PyAudio()

	def run(s):
		stream = s.p.open(format=s.p.get_format_from_width(s.f.getsampwidth()),
						channels=s.f.getnchannels(),
						rate=s.f.getframerate(),
						output=True)

		while True:
			data = s.f.readframes(s.chunk)
			stream.write(data)
			if not data:
				break

		stream.stop_stream()
		stream.close()

		s.p.terminate()

import numpy as np


def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class LightPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)

		s.b = phue.Bridge('192.168.1.211')
		s.b.connect()

		# chroma, _, sr, _ = pychorus.create_chroma(path)
		# time_time_similarity = similarity_matrix.TimeTimeSimilarityMatrix(chroma, sr)
		# time_lag_similarity = similarity_matrix.TimeLagSimilarityMatrix(chroma, sr)
		#
		# time_time_similarity.display()
		# time_lag_similarity.display()

		# f = wave.open(path, 'r')
		# track_length = f.getnframes() / f.getframerate()

		s.map = []
		# for i in range(int(track_length*10)):
		# 	j = int(track_length*10 / len(time_time_similarity.matrix))
		# 	slice = []
		# 	slice += [0.5]
		# 	# slice += [sum(time_time_similarity.matrix[j])/len(time_time_similarity.matrix[j])]
		# 	# slice += [sum(time_lag_similarity.matrix[j])/len(time_lag_similarity.matrix[j])]
		# 	slice += [time_time_similarity.matrix[j][10]]
		# 	slice += [time_lag_similarity.matrix[j][10]]
		# 	s.map += [slice]

		wr = wave.open(path, 'r')
		music = wave.open(path, 'r')

		frame_rate = 10
		sample_size = music.getframerate() // frame_rate  # Read and process 1/fr second at a time.
		# A larger number for fr means less reverb.
		number_of_slices = int(music.getnframes() / sample_size)  # count of the whole file

		for slice_number in range(number_of_slices):
			da = np.fromstring(music.readframes(sample_size), dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			# lf, rf = np.fft.rfftfreq(left), np.fft.rfftfreq(right)

			sample = left
			# sample /= 1500

			graph = np.abs(np.fft.rfft(sample).real)
			a = sigmoid(graph) * 2 - 1


			# w = np.fft.rfft(left)
			# freqs = np.fft.rfftfreq(len(w))
			# track_length = len(left)
			#
			# l = len(freqs)

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

			graph1 = graph1[min:max]

			points_x = []
			points_y = []
			for i in range(l):
				freq = graph1[i]
				theta = i / l
				theta *= (5 / 6)  # *5/6 cuts pink from the rainbow
				theta *= math.pi * 2
				points_x += [freq * math.sin(theta)]
				points_y += [freq * math.cos(theta)]
			# freqs = np.fft.fftfreq(len(graph1))

			x = np.sum(points_x) / len(points_x)
			y = np.sum(points_y) / len(points_y)
			z = math.sqrt(x * x + y * y)
			print(x, y, z)

			hue = (math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)
			sat = math.sqrt(x**2 + y**2)
			# bri = sum(freqs)/l
			bri = z

			if slice_number%1 == 0:
				fig, ax1 = plt.subplots()

				ax1.plot(range(len(a)), a, color='m')
				# ax1.plot(range(len(b)), b, color='g')

				# ax2 = ax1.twinx()
				# ax2.plot(range(len(b)), b, color='g')

				# fig.legend(['w', 'f'])
				# fig.tight_layout()
				fig.show()
				pass

			s.map += [[hue, sat, bri]]

	def run(s):
		start = time.time()

		i = 0
		for slice in s.map:
			command = {
				'transitiontime': 1,
				'hue': int(slice[0] * 65535),
				'sat': int(slice[1] * 254),
				'bri': int(slice[2] * 254)
			}
			print(command)
			s.b.set_light('cal', command)
			i+=1
			time.sleep(start + (i/10) - time.time())



def test():
	path = "./audio/toto_africa.wav"

	mPlayer = MusicPlayer(path)
	lPlayer = LightPlayer(path)

	mPlayer.start()
	lPlayer.run()


if __name__ == '__main__':
	# run()
	test()



