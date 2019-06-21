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

class ButtonManager():
	def __init__(s):
		pygame.init()
		# surface = pygame.display.set_mode((400, 300), 0, 32)

		pygame.joystick.init()
		s.joysticks = []
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			print("Initialised: ", joystick.get_name())
			s.joysticks += [joystick]

		s.base = 0
		s.last = 0
		s.offset = 0
		s.button_hot = [False] * s.joysticks[0].get_numbuttons()

		s.recorded = []
		s.replay = False


		s.count = 0


	def update(s):
		pygame.event.pump()

		s.temp = {
			"axis": [s.joysticks[0].get_axis(i) for i in range(s.joysticks[0].get_numaxes())],  # todo add correctJoy()
			"balls": [s.joysticks[0].get_ball(i) for i in range(s.joysticks[0].get_numballs())],
			"buttons": [s.joysticks[0].get_button(i) for i in range(s.joysticks[0].get_numbuttons())],
			"hats": [s.joysticks[0].get_hat(i) for i in range(s.joysticks[0].get_numhats())],
		}

		if s.replay:
			s.temp["axis"] = s.recorded[s.count % len(s.recorded)]

		for i in range(s.joysticks[0].get_numbuttons()):
			if s.temp["buttons"][i]:
				if not s.button_hot[i]:
					s.button_hot[i] = True
					if i == 0:
						s.base = random.uniform(0, 1)
					if i == 1:
						s.last = (((1+s.temp["axis"][0]) / 2)+s.offset) % 1
					if i == 4:
						if len(s.recorded) > 0:
							s.replay = not s.replay
					if i == 2:
						s.recorded = []
						s.replay = False
			else:

				if s.button_hot[i]:
					s.button_hot[i] = False

		if s.button_hot[2]:
			s.recorded += [s.temp["axis"]]

		if s.button_hot[1]:
			s.offset = (s.last-((1+s.temp["axis"][0]) / 2)) % 1

		# command = (
		# 	1-s.temp["axis"][3],
		# 	(s.base+(((1+s.temp["axis"][0]) / 2)+s.offset)) % 1,
		# 	1-s.temp["axis"][1]
		# )
		s.count += 1
		return s.temp["axis"]


class MusicPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)
		s.mf = wave.open(path, 'r')
		s.chunk = 1024
		s.p = pyaudio.PyAudio()
		s.LIVE = True
		s.JOY = True
		if s.LIVE:
			s.lf = wave.open(path, 'r')
			s.lp = LivePlayer()
			if s.JOY:
				s.bm = ButtonManager()

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
					if s.JOY:
						controls = np.array(s.bm.update())
						# controls **= 2
						controls *= 3
						# print(controls)
						s.lp.light_player.hueCo = 1 / (2 + controls[0])
						s.lp.light_player.satCo = 1 / (3 + (1-controls[1]))
						s.lp.light_player.velocity = 4.9 + (controls[2])
						s.lp.light_player.curve = (1 + controls[3])
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

		s.velocity = 4.9
		s.curve = 1
		s.cap = 1.5
		s.cutoff = 0.96
		s.hueCo = (1 / 2)
		s.satCo = (1 / 3)

	def gen_slice(s, sample, frame_rate):
		scaler = 10**s.velocity

		limit = scaler / frame_rate
		sample = sample / limit

		graph = np.abs(np.fft.rfft(sample).real) #** (1 / co)
		graph1 = sigmoid(graph) * 2 - 1
		graph1 **= s.curve

		min = 0
		# max = int(limit)
		max = int(len(graph1)/s.cap)

		l = max - min
		graph1 = graph1[min:max]

		points_x = []
		points_y = []
		for i in range(l):
			freq = graph1[i]
			theta = i / l
			theta *= s.cutoff  # cuts pink from the rainbow
			theta *= math.pi * 2
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]

		x = np.sum(points_x) / len(points_x)
		y = np.sum(points_y) / len(points_y)

		hue = ((math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)) ** s.hueCo
		sat = math.sqrt((x * x) + (y * y)) ** s.satCo
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
		# print(command)

	def run(s):
		start = time.time()

		i = 0
		for slice in s.map:
			s.send_map(slice)
			i+=1
			wait = start + (i/10) - time.time()
			if wait > 0:
				time.sleep(wait)


def test1(path):
	lPlayer = LightPlayer()
	lPlayer.generate(path)

	fig, ax1 = plt.subplots()
	ax1.plot(range(len(lPlayer.map)), [bri for hue, sat, bri in lPlayer.map], color='b')
	ax1.plot(range(len(lPlayer.map)), [hue for hue, sat, bri in lPlayer.map], color='r')
	ax1.plot(range(len(lPlayer.map)), [sat for hue, sat, bri in lPlayer.map], color='g')
	fig.show()


def test2(path):
	mPlayer = MusicPlayer(path)
	lPlayer = LightPlayer()
	lPlayer.load()

	mPlayer.start()
	lPlayer.run()


def test3(path):
	mPlayer = MusicPlayer(path)
	mPlayer.run()


if __name__ == '__main__':
	# path = "./audio/mass.wav"
	path = "./audio/kuzz.wav"	# run()
	test1(path)
	# test2(path)
	# test3(path)



