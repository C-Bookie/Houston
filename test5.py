from picamera import PiCamera
from PIL import Image
from time import sleep
import pysstv
import pygame

camera = PiCamera()

image_path = './images/capture.jpg'

if __name__== "__main__":
	camera.capture(image_path)
	image = Image.open(open(image_path, 'rb'))
	sstv = pysstv.sstv(image)
	sstv.write_wav()

	pygame.mixer.init()
	pygame.mixer.music.load("myFile.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

