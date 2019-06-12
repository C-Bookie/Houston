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

import pychorus
from pychorus import similarity_matrix


def test():
	path = "./music/in_game_music_1.wav"
	# path = "./music/in_game_music_2.wav"
	# path = "./music/main_menu_music.wav"
	# path = "./music/loading.wav"

	mPlayer = MusicPlayer(path)
	lPlayer = LightPlayer(path)

	mPlayer.start()
	lPlayer.run()


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


class LightPlayer(threading.Thread):
	def __init__(s, path):
		threading.Thread.__init__(s)

		s.b = phue.Bridge('192.168.1.211')
		s.b.connect()

		chroma, _, sr, _ = pychorus.create_chroma(path)
		time_time_similarity = similarity_matrix.TimeTimeSimilarityMatrix(chroma, sr)
		time_lag_similarity = similarity_matrix.TimeLagSimilarityMatrix(chroma, sr)

		f = wave.open(path, 'r')
		track_length = f.getnframes() / f.getframerate()

		s.map = []
		for i in range(int(track_length*10)):
			slice = []
			slice += [0.5]
			slice += [sum(time_time_similarity.matrix[i])/len(time_time_similarity.matrix[i])]
			slice += [sum(time_lag_similarity.matrix[i])/len(time_lag_similarity.matrix[i])]
			s.map += [slice]


	def run(s):
		start = time.time()

		i = 0
		for slice in s.map:
			command = {
				'transitiontime': 1,
				'bri': int(slice[0] * 254),
				'hue': int(slice[1] * 65535),
				'sat': int(slice[2] * 254)
			}
			s.b.set_light('cal', command)
			i+=1
			time.sleep(start + (i/10) - time.time())


if __name__ == '__main__':
	# run()
	test()
