#testing phue and mqtt for motion sensing lights

#TODO
#merge audio streams
#add audio input stream
#impliment spotify steam

#finish lightRiderGym
#develop flame for stream/training
#develpo multi dimentional (1<D) grids

#add TCP music stream
#intergrate into huston





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
GEN_GRAPHS = False


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
		# s.button_hot = [False] * s.joysticks[0].get_numbuttons()

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

		if 0:

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


#https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo.py
def openStream():
	defaultframes = 512

	class textcolors:
		blue = '\033[94m'
		green = '\033[92m'
		warning = '\033[93m'
		fail = '\033[91m'
		end = '\033[0m'

	useloopback = False

	# Use module
	p = pyaudio.PyAudio()

	# Set default to first in list or ask Windows
	try:
		default_device_index = p.get_default_input_device_info()
	except IOError:
		default_device_index = -1


	if 1:
		# Select Device
		print(textcolors.blue + "Available devices:\n" + textcolors.end)
		for i in range(0, p.get_device_count()):
			info = p.get_device_info_by_index(i)
			print(textcolors.green + str(info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (
			info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

			if default_device_index == -1:
				default_device_index = info["index"]

		# Handle no devices available
		if default_device_index == -1:
			print(textcolors.fail + "No device available. Quitting." + textcolors.end)
			exit()

		# Get input or default
		device_id = int(input("Choose device [" + textcolors.blue + str(
			default_device_index) + textcolors.end + "]: ") or default_device_index)
	else:
		device_id = 9
	print("")

	# Get device info
	try:
		device_info = p.get_device_info_by_index(device_id)
	except IOError:
		device_info = p.get_device_info_by_index(default_device_index)
		print(textcolors.warning + "Selection not available, using default." + textcolors.end)

	# Choose between loopback or standard mode
	is_input = device_info["maxInputChannels"] > 0
	is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
	if is_input:
		print(textcolors.blue + "Selection is input using standard mode.\n" + textcolors.end)
	else:
		if is_wasapi:
			useloopback = True
			print(textcolors.green + "Selection is output. Using loopback mode.\n" + textcolors.end)
		else:
			print(
				textcolors.fail + "Selection is output and does not support loopback mode. Quitting.\n" + textcolors.end)
			exit()

	# Open stream
	channelcount = device_info["maxInputChannels"] if (
				device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info[
		"maxOutputChannels"]
	stream = p.open(format=pyaudio.paInt16,
					channels=channelcount,
					rate=int(device_info["defaultSampleRate"]),
					input=True,
					frames_per_buffer=defaultframes,
					input_device_index=device_info["index"],
					as_loopback=useloopback)

	return stream


class MusicPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)
		s.USE_WAV = True
		s.OUTPUT = True
		if s.USE_WAV:
			s.f = wave.open(path, 'r')
			s.sampleWidth = s.f.getsampwidth()
			s.channels = s.f.getnchannels()
			s.framerate = s.f.getframerate()


		s.chunk = 1024
		s.p = pyaudio.PyAudio()
		s.LIVE = False
		s.JOY = True
		if s.LIVE:
			# s.lf = wave.open(path, 'r')
			s.lp = LivePlayer()
			if s.JOY:
				s.bm = ButtonManager()

	def run(s):
		if not s.USE_WAV:
			in_stream = openStream()

			s.sampleWidth = 44000
			s.framerate = 10


		next = s.f.readframes(s.chunk)

		mi = 0
		if s.LIVE:
			frame_rate = 10
			sample_size = s.f.getframerate() // frame_rate
			number_of_slices = int(s.f.getnframes() / sample_size)

			li = 0
			s.lp.start()
			s.lp.queue.put(next)

			if s.USE_WAV:
				s.chunk = sample_size


		if s.OUTPUT:
			out_stream = s.p.open(format=s.p.get_format_from_width(s.sampleWidth),
				channels=s.channels,
				rate=s.framerate,
				output=True)

		if s.USE_WAV:
			skip = 00
			s.f.setpos(s.chunk * skip)
			mi = skip

		while True:
			data = next
			if s.USE_WAV:
				next = s.f.readframes(s.chunk)
			else:
				next = in_stream.read(int(sample_size/1.1))
			if s.LIVE:
				if (mi+1)*s.chunk > li*sample_size:
					s.lp.queue.join()
					s.lp.light_player.send_map_slice(s.lp.slice)
					# ldata = s.lf.readframes(sample_size)
					ldata = next
					if s.JOY:
						controls = np.array(s.bm.update())
						# controls **= 2
						controls *= 3
						# print(controls)
						s.lp.light_player.hueCo = 1 / (2 + controls[0])
						s.lp.light_player.satCo = 1 / (3 + (1-controls[1]))
						s.lp.light_player.velocity = 4.9 + (controls[2])
						s.lp.light_player.curve = (1 + controls[3])

						# s.lp.light_player.hueCo = 1 / (2 + controls[0])
						# s.lp.light_player.satCo = 1 / (3 + (1-controls[1]))
						# s.lp.light_player.velocity = 4.9 + (controls[3])
						# s.lp.light_player.curve = (1 + controls[4])
					s.lp.queue.put(ldata)
					li += 1
			mdata = data
			if s.OUTPUT:
				out_stream.write(mdata)
			if not mdata:
				break

			if mi % 10 == 0:
				print(mi)

			mi += 1

		out_stream.stop_stream()
		out_stream.close()

		s.p.terminate()


def sigmoid(x):
	return 1 / (1 + np.exp(-x))


class LivePlayer(threading.Thread):
	def __init__(s):
		threading.Thread.__init__(s)
		s.fr = 10
		s.slice = (0, 0, 0)
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


class LightPlayer(threading.Thread):
	def __init__(s):
		threading.Thread.__init__(s)
		s.b = phue.Bridge('192.168.1.227')
		s.b.connect()

		s.velocity = 4.7  # lower is brighter
		s.curve = 2
		s.cap = 1.5
		s.start = 0.0
		s.cutoff = 0.97
		s.hueCo = (1 / 2)
		s.satCo = (1 / 3)

		# s.velocity = 4.4
		# s.curve = 3
		# s.cap = 1.5
		# s.start = 0.7
		# s.cutoff = 0.96
		# s.hueCo = (1 / 2)
		# s.satCo = (1 / 3)

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
			theta *= s.cutoff - s.start  # cuts pink from the rainbow
			theta += s.start
			theta *= math.pi * 2
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]

		x = np.sum(points_x) / len(points_x)
		y = np.sum(points_y) / len(points_y)

		hue = ((math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)) ** s.hueCo
		sat = math.sqrt((x * x) + (y * y)) ** s.satCo
		bri = sum(sigmoid(abs(sample)) * 2 - 1) / len(sample)

		if GEN_GRAPHS:
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

	def generate_map(s, path):
		music = wave.open(path, 'r')

		frame_rate = 10
		sample_size = music.getframerate() // frame_rate  # Read and process 1/fr second at a time.
		# A larger number for fr means less reverb.
		number_of_slices = int(music.getnframes() / sample_size)  # count of the whole file

		s.map = []

		for _slice_number in range(number_of_slices):
			da = np.fromstring(music.readframes(sample_size), dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			# sample = (left + right) / 2
			sample = left
			s.map += [s.gen_slice(sample, frame_rate)]
		np.save('map.npy', s.map)

	def load(s):
		s.map = np.load('map.npy')

	def send_map_slice(s, slice):
		# print(slice)

		on = True
		# on = (True if (map[2] > 1/254) else False)
		command = {
			'transitiontime': 1,
			'hue': int(slice[0] * 65535),
			'sat': int(slice[1] * 254),
			'bri': int(slice[2] * 254),
			'on': on
		}
		s.b.set_light('cal', command)
		# print(command)

	def run(s):
		start = time.time()

		i = 0
		for slice in s.map:
			s.send_map_slice(slice)
			i+=1
			wait = start + (i/10) - time.time()
			if wait > 0:
				time.sleep(wait)



def test1(path):
	lPlayer = LightPlayer()
	lPlayer.generate_map(path)

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

def test4():
	lPlayer = LightPlayer()
	i = 0
	start = time.time()
	fr = 10
	lag = []

	while True:
		if i%fr == 0:
			if len(lag) == 0:
				avg_lag = 0
			else:
				avg_lag = sum(lag)/len(lag)
			print(i//fr, ": \t", avg_lag)
			lag = []
			slice = (
				1,
				0.5,
				1
			)
		else:
			slice = (
				1 - ((i%fr)/fr),
				0.5,
				# 1 - (1/(i%fr))
				1
			)

		lPlayer.send_map_slice(slice)
		i += 1

		wait = start + (i/fr) - time.time()
		if wait > 0:
			time.sleep(wait)
		else:
			lag += [-wait]


if __name__ == '__main__':
	path = "./audio/mass.wav"
	# path = "./audio/kuzz.wav"	# run()
	# path = "./audio/mozart.wav"
	# path = "./audio/dubwise.wav"
	# path = "./audio/birdy.wav"
	# test1(path)
	test2(path)
	# test3(path)
	# test4()



