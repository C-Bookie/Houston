#testing phue and mqtt for motion sensing lights
import threading
import wave
from queue import Queue

import math
import phue
import time
import random

import numpy as np

import pyaudio as pyaudio
import pygame

import matplotlib.pyplot as plt


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
		s.mf = wave.open(path, 'r')
		s.chunk = 1024
		s.p = pyaudio.PyAudio()
		s.LIVE = True
		if s.LIVE:
			s.lf = wave.open(path, 'r')
			s.lp = LivePlayer()

	def run(s):
		stream = s.p.open(format=s.p.get_format_from_width(s.mf.getsampwidth()),
						channels=s.mf.getnchannels(),
						rate=s.mf.getframerate(),
						output=True)

		mi = 0
		if s.LIVE:
			frame_rate = 10
			sample_size = s.lf.getframerate() // frame_rate
			number_of_slices = int(s.lf.getnframes() / sample_size)

			li = 0
			s.lp.start()
			ldata = s.lf.readframes(sample_size)
			s.lp.queue.put(ldata)
		while True:
			if s.LIVE:
				if (mi+1)*s.chunk > li*sample_size:
					s.lp.queue.join()
					s.lp.send_map()
					ldata = s.lf.readframes(sample_size)
					s.lp.queue.put(ldata)
					li += 1
			mdata = s.mf.readframes(s.chunk)
			stream.write(mdata)
			if not mdata:
				break
			mi += 1

		stream.stop_stream()
		stream.close()

		s.p.terminate()

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class LivePlayer(threading.Thread):
	def __init__(s):
		threading.Thread.__init__(s)
		s.fr = 10
		s.map = (0, 0, 0)
		s.queue = Queue()
		s.light_player = LightPlayer()

	def run(s):
		while True:
			data = s.queue.get()
			if not data:
				break
			da = np.fromstring(data, dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			sample = left
			s.map = s.light_player.gen_slice(sample, s.fr)
			s.queue.task_done()
		s.queue.task_done()

	def send_map(s):
		s.light_player.send_map(s.map)



class LightPlayer(threading.Thread):
	def __init__(s):
		threading.Thread.__init__(s)
		s.b = phue.Bridge('192.168.1.211')
		s.b.connect()
		s.map = []

	def gen_slice(s, sample, frame_rate):
		scaler = 10**4.9

		limit = scaler / frame_rate
		sample = sample / limit

		graph = np.abs(np.fft.rfft(sample).real) #** (1 / co)
		graph1 = sigmoid(graph) * 2 - 1

		min = 0
		# max = int(limit)
		max = int(len(graph1)/1.5)

		l = max - min
		graph1 = graph1[min:max]

		points_x = []
		points_y = []
		for i in range(l):
			freq = graph1[i]
			theta = i / l
			theta *= 0.96  # cuts pink from the rainbow
			theta *= math.pi * 2
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]

		x = np.sum(points_x) / len(points_x)
		y = np.sum(points_y) / len(points_y)

		hue = ((math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)) ** (1/2)
		sat = math.sqrt((x * x) + (y * y)) ** (1 / 3)
		bri = sum(sigmoid(abs(sample)) * 2 - 1) / len(sample)

		if 0:
			print(hue, sat, bri)

			fig, ax1 = plt.subplots()
			ax1.plot(range(len(graph)), graph, color='b')
			fig.show()

			fig, ax2 = plt.subplots()
			ax2.plot(range(len(graph1)), graph1, color='b')
			fig.show()

			fig, ax3 = plt.subplots()
			ax3.plot(points_x, points_y, color='b')
			ax3.scatter(0, 0)
			ax3.scatter(x, y)
			fig.show()

			# ax2 = ax1.twinx()
			fig, ax2 = plt.subplots()
			ax2.plot(range(len(sample)), sample, color='g')
			# ax2.plot(range(len(freqs)), freqs, color='b')
			fig.show()

		return (hue, sat, bri)

	def generate(s, path):
		music = wave.open(path, 'r')

		frame_rate = 10
		sample_size = music.getframerate() // frame_rate  # Read and process 1/fr second at a time.
		# A larger number for fr means less reverb.
		number_of_slices = int(music.getnframes() / sample_size)  # count of the whole file

		for _slice_number in range(number_of_slices):
			da = np.fromstring(music.readframes(sample_size), dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			# sample = (left + right) / 2
			sample = left
			s.map += [s.gen_slice(sample, frame_rate)]
		np.save('map.npy', s.map)

	def load(s):
		s.map = np.load('map.npy')

	def send_map(s, map):
		command = {
			'transitiontime': 1,
			'hue': int(map[0] * 65535),
			'sat': int(map[1] * 254),
			'bri': int(map[2] * 254)
		}
		s.b.set_light('cal', command)
		print(command)

	def run(s):
		start = time.time()

		i = 0
		for slice in s.map:
			s.send_map(slice)
			i+=1
			wait = start + (i/10) - time.time()
			if wait > 0:
				time.sleep(wait)


def test1():
	path = "./audio/mass.wav"
	lPlayer = LightPlayer()
	lPlayer.generate(path)

	fig, ax1 = plt.subplots()
	ax1.plot(range(len(lPlayer.map)), [bri for hue, sat, bri in lPlayer.map], color='b')
	ax1.plot(range(len(lPlayer.map)), [hue for hue, sat, bri in lPlayer.map], color='r')
	ax1.plot(range(len(lPlayer.map)), [sat for hue, sat, bri in lPlayer.map], color='g')
	fig.show()


def test2():
	path = "./audio/mass.wav"
	mPlayer = MusicPlayer(path)
	lPlayer = LightPlayer()
	lPlayer.load()

	mPlayer.start()
	lPlayer.run()


def test3():
	path = "./audio/mass.wav"
	mPlayer = MusicPlayer(path)
	mPlayer.run()


if __name__ == '__main__':
	# run()
	# test1()
	# test2()
	test3()



