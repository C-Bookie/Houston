import threading

PI=False

if PI:
	from picamera import PiCamera
from PIL import Image
from time import sleep
import pysstv.color
import pygame

if PI:
	camera = PiCamera()

path = 'capture'

class Generator(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.new = threading.Event()
		self.i = 0
		self.latest = ""

	def run(self):
		while True:
			cur_path = path + str(self.i).zfill(6)
			image_path = "./images/" + cur_path + ".jpg"
			audio_path = "./audio/" + cur_path + ".wav"
			if PI:
				print(cur_path, " | Capturing")
				camera.exposure_mode = 'auto'
				camera.capture(image_path)
			image = Image.open(open("./images/" + cur_path + ".jpg", 'rb'))
			print(cur_path, " | Converting")
			sstv = pysstv.color.Robot36(image, 48000, 16)
			print(cur_path, " | Saving")
			sstv.write_wav(audio_path)
			self.latest = cur_path
			self.i+=1
			self.new.set()
			if not PI:
				break


if __name__== "__main__":
	pygame.mixer.init()
	gen = Generator()
	gen.start()

	while True:
		gen.new.wait()
		# gen.new.clear()
		print(gen.latest, " | Playing")
		pygame.mixer.music.load("./audio/" + gen.latest + ".wav")
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			sleep(1)
		sleep(1)

