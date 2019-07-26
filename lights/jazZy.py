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
#research https://gist.github.com/nabeel913/344fa7a501f9eef6d6090aa20b00d954

import colorsys
import sys
import threading
import wave
from queue import Queue

import math
import phue
import time
import random
import queue

import numpy as np

import pyaudio as pyaudio
import pygame
from pygame.locals import *

import matplotlib.pyplot as plt

import connection

deadzone = 0.25
GEN_GRAPHS = False


def sigmoid(x):
	return 1 / (1 + np.exp(-x))

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

		s.count += 1
		return s.temp["axis"]


#https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo.py
def openInputStream(id=None, framerate=None):
	useloopback = False

	p = pyaudio.PyAudio()

	try:
		default_device_index = p.get_default_input_device_info()
	except IOError:
		default_device_index = -1


	if id is None:
		for i in range(0, p.get_device_count()):
			info = p.get_device_info_by_index(i)
			print(str(info["index"]) + ":  \t %s \t %s" % (p.get_host_api_info_by_index(info["hostApi"])["name"], info["name"]))

			if default_device_index == -1:
				default_device_index = info["index"]

		# Handle no devices available
		if default_device_index == -1:
			print("No device available. Quitting.")
			exit()

		# Get input or default
		device_id = int(input("Choose Input device: ") or default_device_index)
	else:
		device_id = id
	print("")

	# Get device info
	try:
		device_info = p.get_device_info_by_index(device_id)
	except IOError:
		device_info = p.get_device_info_by_index(default_device_index)
		print("Selection not available, using default.")

	# Choose between loopback or standard mode
	is_input = device_info["maxInputChannels"] > 0
	is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
	if is_input:
		print("Selection is input using standard mode.\n")
	else:
		if is_wasapi:
			useloopback = True
			print("Selection is output. Using loopback mode.\n")
		else:
			print("Selection is output and does not support loopback mode. Quitting.\n")
			exit()

	# Open stream
	channelcount = device_info["maxInputChannels"] if (
				device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info[
		"maxOutputChannels"]
	if framerate is None:
		frames_per_buffer = 1024
	else:
		frames_per_buffer = int(device_info["defaultSampleRate"] / framerate)

	stream = p.open(format=pyaudio.paInt16,
					channels=channelcount,
					rate=int(device_info["defaultSampleRate"]),
					input=True,
					frames_per_buffer=frames_per_buffer,
					input_device_index=device_info["index"],
					as_loopback=useloopback)

	return stream, device_info


def openOutpoutStream(id=None, framerate=None):
	p = pyaudio.PyAudio()

	try:
		default_device_index = p.get_default_output_device_info()["index"]
	except IOError:
		default_device_index = -1


	if id is None:
		for i in range(0, p.get_device_count()):
			info = p.get_device_info_by_index(i)
			print(str(info["index"]) + ":  \t %s \t %s" % (p.get_host_api_info_by_index(info["hostApi"])["name"], info["name"]))

			if default_device_index == -1:
				default_device_index = info["index"]

		# Handle no devices available
		if default_device_index == -1:
			print("No device available. Quitting.")
			exit()

		# Get input or default
		device_id = int(input("Choose output device: ") or default_device_index)
	else:
		device_id = id
	print("")

	# Get device info
	try:
		device_info = p.get_device_info_by_index(device_id)
	except IOError:
		device_info = p.get_device_info_by_index(default_device_index)
		print("Selection not available, using default.")

	# Choose between loopback or standard mode
	is_output = device_info["maxOutputChannels"] > 0
	if device_info["maxOutputChannels"] == 0:
		print("not an output.\n")
		exit()

	# Open stream
	# channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
	channelcount = 2
	if framerate is None:
		frames_per_buffer = 1024
	else:
		frames_per_buffer = int(device_info["defaultSampleRate"] / framerate)

	stream = p.open(format=pyaudio.paInt16,
					channels=channelcount,
					rate=int(device_info["defaultSampleRate"]),
					output=True,
					frames_per_buffer=frames_per_buffer,
					output_device_index=device_info["index"])

	return stream, device_info

class Pacer():
	def __init__(s, fr):
		s.fr = fr
		s.i = 0
		s.lag = []
		s.start = time.time()

	def wait(s):
		if s.i % s.fr == 0:
			if len(s.lag) == 0:
				avg_lag = 0
			else:
				avg_lag = sum(s.lag) / len(s.lag)
			print(s.i // s.fr, ": \t", avg_lag)
			s.lag = []

		s.i += 1

		wait = s.start + (s.i / s.fr) - time.time()
		if wait > 0:
			time.sleep(wait)
		s.lag += [wait]

class LiveInputStream(threading.Thread):
	def __init__(s, stream, chunk):
		threading.Thread.__init__(s)
		s.stream = stream
		s.chunk = chunk
		s.queue = queue.Queue()

	def run(s):
		while True:
			s.queue.put(s.stream.read(s.chunk))

class MusicPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)
		s.USE_WAV = False
		s.OUTPUT = True
		if s.USE_WAV:
			s.f = wave.open(path, 'r')

		s.chunk = 1024
		s.p = pyaudio.PyAudio()
		s.LIVE = True
		s.MILL = False
		s.JOY = False
		if s.LIVE:
			# s.lf = wave.open(path, 'r')
			s.live_mapper = LiveMapper(s.MILL)
			s.light_player = LightPlayer()
			if s.JOY:
				s.bm = ButtonManager()


	def run(s):
		frame_rate = 10
		pacer = Pacer(frame_rate)

		if not s.LIVE:
			frame_rate = None

		if s.USE_WAV:
			s.sampleWidth = s.f.getsampwidth()
			s.channels = s.f.getnchannels()
			s.framerate = s.f.getframerate()
		else:
			in_stream, input_info = openInputStream(9, frame_rate)
			s.channels = input_info["maxOutputChannels"]
			s.sampleWidth = s.channels
			s.framerate = int(input_info["defaultSampleRate"])

		if s.LIVE:
			li = 0
			s.chunk = s.framerate // frame_rate
			s.live_mapper.start()
			s.light_player.start()
		else:
			frame_rate = s.framerate // s.chunk


		if s.OUTPUT:
			out_stream, output_info = openOutpoutStream(9, frame_rate)

		mi = 0
		if s.USE_WAV:
			skip = 00
			s.f.setpos(s.chunk * skip)
			mi = skip
			next = s.f.readframes(s.chunk)
		else:
			s.live_input_stream = LiveInputStream(in_stream, s.chunk)
			s.live_input_stream.start()
			next = s.live_input_stream.queue.get()

		if s.LIVE:
			s.live_mapper.queue.put(next)


		while True:
			data = next
			if s.USE_WAV:
				next = s.f.readframes(s.chunk)
			else:
				next = s.live_input_stream.queue.get()
			if s.LIVE:
				if (mi+1)*s.chunk > li*s.chunk:
					s.live_mapper.queue.join()
					s.light_player.send_map_slice(s.live_mapper.slice)
					if s.JOY:
						controls = np.array(s.bm.update())
						# controls **= 2
						controls *= 3
						# print(controls)
						s.live_mapper.hueCo = 1 / (2 + controls[0])
						s.live_mapper.satCo = 1 / (3 + (1-controls[1]))
						s.live_mapper.velocity = 4.9 + (controls[2])
						s.live_mapper.curve = (1 + controls[3])

						# s.lp.light_player.hueCo = 1 / (2 + controls[0])
						# s.lp.light_player.satCo = 1 / (3 + (1-controls[1]))
						# s.lp.light_player.velocity = 4.9 + (controls[3])
						# s.lp.light_player.curve = (1 + controls[4])
					s.live_mapper.queue.put(next)
					li += 1
			if s.OUTPUT:
				out_stream.write(data * 0.5)
			if not data:
				break

			pacer.wait()
			mi +=1

		out_stream.stop_stream()
		out_stream.close()

		s.p.terminate()


class LightPlayer(threading.Thread):
	def __init__(s, bridgeIP=None, screen=True):
		threading.Thread.__init__(s)
		bridgeIP = '192.168.1.211'
		if bridgeIP is not None:
			s.b = phue.Bridge(bridgeIP)
			s.b.connect()
		else:
			s.b = None

		if screen:
			s.height = 300
			s.width = 400

			pygame.init()
			s.display = pygame.display.set_mode((s.width, s.height))#, pygame.FULLSCREEN)
			pygame.display.set_caption('jazZy')
		else:
			s.display = None

		s.map = []


	def send_map_slice(s, slice):
		if s.b is not None:
			command = {
				'transitiontime': 1,
				'hue': int(slice[0] * 65535),
				'sat': int(slice[1] * 254),
				'bri': int(slice[2] * 254),
			}
			s.b.set_light('cal', command)
			# s.b.set_light('conservitory', command)
			# print(command)

		if s.display is not None:
			r, g, b = colorsys.hsv_to_rgb(*slice)
			colour = (255*r, 255*g, 255*b)
			s.display.fill(colour)
			# z = np.array([[colour]*20]*20 )
			# # z = np.array([[colour]*s.width]*s.height)
			# # z = np.array([[colour for x in range(-s.width // 2, s.width // 2)] for y in range(-s.height // 2, s.height // 2)])

			# surf = pygame.surfarray.make_surface(z)
			# pygame.transform.smoothscale(surf, (200, s.height))

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					# sys.exit()
			# s.display.blit(surf, (0, 0))
			pygame.display.update()

	def run(s):
		start = time.time()
		fr = 10
		lag = []

		i = 0
		for slice in s.map:
			s.send_map_slice(slice)

			if i % fr == 0:
				if len(lag) == 0:
					avg_lag = 0
				else:
					avg_lag = sum(lag) / len(lag)
				print(i // fr, ": \t", avg_lag)
				lag = []

			i+=1
			wait = start + (i/fr) - time.time()
			if wait > 0:
				time.sleep(wait)
			else:
				lag += [-wait]


class LightMapper():
	def __init__(s, mill=False):
		s.center = (0.1, 0.1, 0.2)

		s.velocity = 4.7  # lower is brighter
		s.curve = 2
		s.cap = 1.5
		s.cutin = 0.0
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

		s.mill = mill
		if s.mill:
			def callback(client, data):
				client.queue.put(connection.decode(data))

			class Requester(connection.Client):
				def __init__(s):
					super().__init__('192.168.1.138')
					# super().__init__('192.168.1.101')
					s.queue = queue.Queue()
					s.callback = callback

				def request(s, data):
					s.send_msg(connection.encode(data))

			s.requester = Requester()
			s.requester.start()


	def gen_slice(s, sample, frame_rate):
		if s.mill:
			s.requester.request({
				"sample": sample.tolist(),
				"frame_rate": frame_rate
			})
			return s.requester.queue.get()
		else:
			return s.process_slice(sample, frame_rate)

	def process_slice(s, sample, frame_rate):
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
			theta *= s.cutoff - s.cutin  # cuts pink from the rainbow
			theta += s.cutin
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

		for slice_number in range(number_of_slices):
			da = np.fromstring(music.readframes(sample_size), dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			# sample = (left + right) / 2
			sample = left
			s.map += [s.gen_slice(sample, frame_rate)]

			if slice_number % 100 == 0:
				print(slice_number)

		return s.map


class LiveMapper(threading.Thread, LightMapper):
	def __init__(s, mill=False):
		LightMapper.__init__(s, mill)
		threading.Thread.__init__(s)
		s.fr = 10
		s.slice = (0, 0, 0)
		s.queue = Queue()

	def run(s):
		while True:
			data = s.queue.get()
			if not data:
				break
			da = np.fromstring(data, dtype=np.int16)
			left, right = da[0::2], da[1::2]  # left and right channel
			sample = right
			s.slice = s.gen_slice(sample, s.fr)
			s.queue.task_done()
		s.queue.task_done()


def test1(path):
	lm = LightMapper()
	map = lm.generate_map(path)
	np.save('map.npy', map)

	fig, ax1 = plt.subplots()
	ax1.plot(range(len(map)), [bri for hue, sat, bri in map], color='b')
	ax1.plot(range(len(map)), [hue for hue, sat, bri in map], color='r')
	ax1.plot(range(len(map)), [sat for hue, sat, bri in map], color='g')
	fig.show()


def test2(path):
	mPlayer = MusicPlayer(path)
	lPlayer = LightPlayer()
	lPlayer.map = np.load('map.npy')

	mPlayer.start()
	lPlayer.run()


def test3(path):
	mPlayer = MusicPlayer(path)
	mPlayer.run()

def test4():
	lPlayer = LightPlayer()
	pacer = Pacer(10)

	while True:
		lPlayer.send_map_slice((
			1 - ((pacer.i % pacer.fr) / pacer.fr),
			0.5,
			1
		))
		pacer.wait()

def test5():
	frame_rate = None
	chunk = 10240

	USE_WAV = True
	OUTPUT = True
	if USE_WAV:
		f = wave.open(path, 'r')
	else:
		in_stream, input_info = openInputStream()
		live_input_stream = LiveInputStream(in_stream, chunk)
		live_input_stream.start()

	out_stream, output_info = openOutpoutStream(8, chunk)

	while True:
		if USE_WAV:
			data = f.readframes(chunk)
		else:
			data = live_input_stream.queue.get()
		out_stream.write(data)

def test6():
	bridgeIP = '192.168.1.211'
	b = phue.Bridge(bridgeIP)
	b.connect()
	api = b.get_api()
	print("moo")


if __name__ == '__main__':
	path = "./audio/mass.wav"
	# path = "./audio/kuzz.wav"	# run()
	# path = "./audio/mozart.wav"
	# path = "./audio/dubwise.wav"
	# path = "./audio/birdy.wav"

	# test1(path)
	# test2(path)
	test3(path)
	# test4()
	# test5()



