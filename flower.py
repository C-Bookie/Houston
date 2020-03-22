import math
import threading

import pygame

# import connection


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

		self.num_points = 1000
		self.points = []

		self.scale = 500
		self.golden_ratio = (1 + 5 ** 0.5) / 2
		# self.turn_fraction = self.golden_ratio
		self.turn_fraction = 0

		self.spacing = 0.5

		self.speed = 0.1 / self.num_points

	def run(self):
		try:
			while True:
				self.loop()
		finally:
			pass
			# self.client.close()

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
				# self.num_points -= 1
				self.speed /= 4
			elif event.type == pygame.KEYUP:
				# self.num_points += 1
				self.speed *= 4
			elif event.type == pygame.QUIT:
				return

		self.turn_fraction += self.speed
		# self.num_points += 1
		self.print()
		self.lock.release()


	def print(self):
		self.screen.blit(self.background, (0, 0))

		# https: // www.youtube.com / watch?v = bqtqltqcQhw

		self.points = []

		for i in range(self.num_points):
			dst = (i / (self.num_points - 1)) ** (1-self.turn_fraction)
			angle = 2 * math.pi * self.turn_fraction * i

			x = dst * math.cos(angle)
			y = dst * math.sin(angle)

			self.points += [(x, y)]

		# for x1, y1 in reversed(self.points):
		# 	for x2, y2 in reversed(self.points):
		# 		dist = 1 - math.sqrt((x1-x2)**2 + (y1-y2)**2) / 2
		# 		central = math.sqrt(((x1+x2)/2)**2 + ((y1+y2)/2)**2) / 2
		# 		bri = (dist**5)*(central**0.5)# ** (central ** 0.5)
		# 		# bri *= 1.1
		# 		colour = (bri*255, bri*255, bri*255)
		# 		point1 = (
		# 			int((self.width/2) + x1 * self.scale),
		# 			int((self.height/2) + y1 * self.scale)
		# 		)
		# 		point2 = (
		# 			int((self.width/2) + x2 * self.scale),
		# 			int((self.height/2) + y2 * self.scale)
		# 		)
		# 		pygame.draw.line(self.screen, colour, point1, point2)

		for i, raw_point in enumerate(self.points):
			x, y = raw_point
			point = (
				int((self.width/2) + x * self.scale),
				int((self.height/2) + y * self.scale)
			)
			# colour = (255, 255, 255)
			r, g, b = 6, 35, 143
			colour = (
				((i % r)/r) * 255,
				((i % g)/g) * 255,
				((i % b)/b) * 255,
			)
			pygame.draw.circle(self.screen, colour, point, 1)

		pygame.display.flip()


# class Template(connection.Client):
# 	def __init__(self):
# 		super().__init__()
# 		self.screen = None
# 		self.white_list_functions += []
#
# 	def connect(self):
# 		super().connect()
# 		self.send_data({
# 			"type": "register",
# 			"args": [
# 				"flower",
# 				2077
# 			]
# 		})


if __name__ == "__main__":
	# tem = Template()
	tem = None
	screen = Screen(tem)
	# tem.screen = screen
	# tem.start()
	screen.run()

