import pygame

from caduceussocket import connection


class RCKeyController(connection.Client):
	def __init__(self):
		super().__init__()

		height = 300
		width = 400

		pygame.init()
		self.screen = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('jazZy')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

		self.key_hot = [False]*4
		self.directions = [
			pygame.K_UP,
			pygame.K_DOWN,
			pygame.K_RIGHT,
			pygame.K_LEFT
		]

		self.white_list_functions += [
			"joy_position"
		]

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				2077,
				"rc_host"
			]
		})

	def run(self):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
					if event.key in self.directions:
						self.key_hot[event.key - self.directions[0]] = event.type == pygame.KEYDOWN

						x = 0
						y = 0

						if self.key_hot[0]:
							y += 1
						if self.key_hot[1]:
							y -= 1
						if self.key_hot[2]:
							x += 1
						if self.key_hot[3]:
							x -= 1

						# I tried to be analog, but annoyingly my finite life has brought me to approximate the digital

						left = y
						right = y

						if x == 1:
							right = abs(right) -1
							left = -(abs(left) -1)
						if x == -1:
							left = abs(left) -1
							right = -(abs(right) -1)

						left *= 1023
						right *= 1023
						left = (int)(left)
						right = (int)(right)

						command = str(left) + '|' + str(right) + '\n'

						self.send_data({
							"type": "broadcast",
							"args": [
								command,
								"rc_car"
							]
						})
				if event.type == pygame.QUIT:
					return

			self.screen.blit(self.background, (0, 0))
			pygame.display.flip()




if __name__ == "__main__":
	host = RCKeyController()
	host.run()
