PI=False

if PI:
	from picamera import PiCamera
from PIL import Image
from time import sleep
import pysstv.color
import pygame

if PI:
	camera = PiCamera()

image_path = './images/capture.jpg'
audio_path = './audio/capture.wav'

if __name__== "__main__":
	i = 0
	while True:
		print(i)
		if PI:
			print("Capturing")
			camera.exposure_mode = 'auto'
			camera.capture(image_path)
		image = Image.open(open(image_path, 'rb'))
		print("Converting")
		sstv = pysstv.color.Robot36(image, 48000, 16)
		print("Saving")
		sstv.write_wav(audio_path)

		print("Playing")
		pygame.mixer.init()
		pygame.mixer.music.load(audio_path)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			sleep(1)
		sleep(1)
		i += 1

