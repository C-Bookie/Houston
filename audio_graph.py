import colorsys

import pygame

import connection


class Screen:
	def __init__(self, client):
		self.client = client

		self.height = 600
		self.width = 800

		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('template')

		pygame.font.init()
		self.font = pygame.font.SysFont('consolas', 25)

		self.back_colour = (32, 32, 32)
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()

		self.points = {
			# "base": ((255, 255, 255), [(0, 0), (self.width, self.height)])
		}

		self.stats = {
			# "base": ((255, 255, 255), "moo")
		}

	def run(self):
		while True:
			self.loop()

	def loop(self):
		events = pygame.event.get()
		# for event in events:
		# 	if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
		# 		self.client.send_data({
		# 			"type": "broadcast",
		# 			"args": [
		# 				{
		# 					"type": "key",
		# 					"args": [
		# 						event.key,
		# 						event.type == pygame.KEYDOWN
		# 					]
		# 				},
		# 				"show_host"
		# 			]
		# 		})
		# 	if event.type == pygame.QUIT:
		# 		return

		# pygame.event.poll()
		self.background.fill(self.back_colour)
		for name in self.points:
			colour, points_set = self.points[name]
			pygame.draw.lines(self.background, colour, False, points_set)
		self.screen.blit(self.background, (0, 0))

		spacing = 20
		drop = 5
		for name in self.stats:
			colour, msg = self.stats[name]
			self.screen.blit(self.font.render(name + ":", False, colour), (10, drop))
			self.screen.blit(self.font.render(msg, False, colour), (150, drop))
			drop += spacing

		pygame.display.flip()


class Graph(connection.Client):
	def __init__(self):
		super().__init__()

		self.screen = None

		self.white_list_functions += [
			"draw"
		]

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"graph",
				2077
			]
		})

	def draw(self, graph, graph1, sample, hsv):
		y_scaler = self.screen.height / max(graph1)
		x_scaler = self.screen.width / (len(graph1)-1)
		y_data = [self.screen.height - (n * y_scaler) for n in graph1]
		x_data = [n * x_scaler for n in range(len(graph1))]
		colour = (64, 255, 64)
		self.screen.points["graph1"] = (colour, list(zip(x_data, y_data)))
		self.screen.stats["graph1"] = (colour, str(max(graph1)))

		y_scaler = self.screen.height / max(graph)
		x_scaler = self.screen.width / (len(graph)-1)
		y_data = [self.screen.height - (n * y_scaler) for n in graph]
		x_data = [n * x_scaler for n in range(len(graph))]
		colour = (255, 64, 64)
		self.screen.points["graph"] = (colour, list(zip(x_data, y_data)))
		self.screen.stats["graph"] = (colour, str(max(graph)))

		y_scaler = self.screen.height / max(sample)  # ignores min
		y_scaler /= 2
		x_scaler = self.screen.width / (len(sample)-1)
		y_data = [(self.screen.height/2) - (n * y_scaler) for n in sample]
		x_data = [n * x_scaler for n in range(len(sample))]
		colour = (64, 64, 255)
		self.screen.points["sample"] = (colour, list(zip(x_data, y_data)))
		self.screen.stats["sample"] = (colour, str(max(sample)))

		h, s, v = hsv
		r, g, b = colorsys.hsv_to_rgb(h, s, v)
		self.screen.back_colour = (r*255, g*255, b*255)
		self.screen.stats["hue"] = ((255, 255, 255), (str(h)))
		self.screen.stats["sat"] = ((255, 255, 255), (str(s)))
		self.screen.stats["bri"] = ((255, 255, 255), (str(v)))

if __name__ == "__main__":
	graph = Graph()
	screen = Screen(graph)
	graph.screen = screen
	graph.start()
	screen.run()
