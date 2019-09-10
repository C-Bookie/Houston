import math
import threading

import pygame

import connection


class Screen:
	def __init__(self, client):
		self.client = client

		self.height = 1000
		self.width = 1000

		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('template')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))

		self.lock = threading.Lock()

		self.num_points = 10000
		self.points = []

		self.scale = 750
		self.turn_fraction = (1 + 5 ** 0.5) / 2

		while True:
			self.print()
			self.turn_fraction += 0.000001
			self.num_points += 1

	def run(self):
		try:
			while True:
				self.loop()
		finally:
			self.client.close()

	def loop(self):
		events = pygame.event.get()
		self.lock.acquire()
		for event in events:
				# self.client.send_data({
				# 	"type": "broadcast",
				# 	"args": [
				# 		{
				# 			"type": "key",
				# 			"args": [
				# 				event.key,
				# 				event.type == pygame.KEYDOWN
				# 			]
				# 		},
				# 		"show_host"
				# 	]
				# })
			if event.type == pygame.KEYDOWN:
				self.num_points -= 1
			elif event.type == pygame.KEYUP:
				self.num_points += 1

			elif event.type == pygame.QUIT:
				return

		self.print()
		self.lock.release()


	def print(self):
		self.screen.blit(self.background, (0, 0))

		# https: // www.youtube.com / watch?v = bqtqltqcQhw

		self.points = []

		for i in range(self.num_points):
			dst = i / (self.num_points - 1)
			angle = 2 * math.pi * self.turn_fraction * i

			x = dst * math.cos(angle)
			y = dst * math.sin(angle)

			self.points += [(x, y)]

		for x, y in self.points:
			point = (
				int((self.width/2) + x * self.scale),
				int((self.height/2) + y * self.scale)
			)
			pygame.draw.circle(self.screen, (255, 255, 255), point, 1)

		pygame.display.flip()


class Template(connection.Client):
	def __init__(self):
		super().__init__()
		self.screen = None
		self.white_list_functions += []

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"flower",
				2077
			]
		})


if __name__ == "__main__":
	# tem = Template()
	tem = None
	screen = Screen(tem)
	# tem.screen = screen
	# tem.start()
	screen.run()

