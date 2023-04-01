import math
import threading
import time

import pygame


class Screen:
	def __init__(self, client):
		self.client = client

		self.height = 1000
		self.width = 1000

		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		# self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
		pygame.display.set_caption('template')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))

		self.lock = threading.Lock()

		self.num_points = 1000
		self.points = []

		self.scale = 500
		self.turn_fraction = 0

		self.spacing = 0.5

		self.speed = 0.05 / self.num_points

		self.max_fps = 60
		self.last_frame = 0

		self.running = True

	def wait(self):
		now = time.time()
		target_time = self.last_frame + 1/self.max_fps
		if now < target_time:
			time.sleep(target_time - now)
			self.last_frame = target_time
		else:
			self.last_frame = now

	def run(self):
		print(self)
		time.sleep(10)
		while self.running:
			self.loop()
			self.wait()

	def loop(self):
		events = pygame.event.get()
		self.lock.acquire()
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.speed /= 4
			elif event.type == pygame.KEYUP:
				self.speed *= 4
			elif event.type == pygame.QUIT:
				self.running = False
				return

		self.turn_fraction += self.speed
		self.print()
		self.lock.release()

	def print(self):
		self.screen.blit(self.background, (0, 0))

		# https://www.youtube.com/watch?v=bqtqltqcQhw

		self.points = []

		for i in range(self.num_points):
			dst = (i / (self.num_points - 1)) ** (1-self.turn_fraction)
			angle = 2 * math.pi * self.turn_fraction * i

			x = dst * math.cos(angle)
			y = dst * math.sin(angle)

			self.points += [(x, y)]

		for i, raw_point in enumerate(self.points):
			x, y = raw_point
			point = (
				int((self.width/2) + x * self.scale),
				int((self.height/2) + y * self.scale)
			)
			r, g, b = 6, 35, 143
			colour = (
				((i % r)/r) * 255,
				((i % g)/g) * 255,
				((i % b)/b) * 255,
			)
			pygame.draw.circle(self.screen, colour, point, 10)

		pygame.display.flip()


if __name__ == "__main__":
	tem = None
	screen = Screen(tem)
	screen.run()
