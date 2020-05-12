import time

import pygame, sys
from pygame.locals import *
import numpy as np

height = 1000
width = 1000

def mandelbrot(r, i):
	c = complex(r, i)
	z = 0     
	n = 0
	MAX_ITER = 100
	while abs(z) <= 2 and n < MAX_ITER:
		z = z*z + c
		n += 1
	colour = 255 - (255 * (n / MAX_ITER))
	return (colour, colour, colour)

if __name__ == '__main__':
	pygame.init()

	# set up the window
	display = pygame.display.set_mode((height, width), 0, 32)
	pygame.display.set_caption('Drawing')

	z = np.array([[mandelbrot(y/(height//2), x/(width//2)) for x in range(-width//2, width//2)] for y in range(-height//2, height//2)])

	surf = pygame.surfarray.make_surface(z)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	display.blit(surf, (0, 0))
	pygame.display.update()

	while True:
		time.sleep(1)