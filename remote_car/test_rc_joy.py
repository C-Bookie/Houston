import time

import pygame

from caduceussocket import connection

dead_zone = 0.25


def correct_joy(n):
	if -dead_zone < n < dead_zone:
		return 0.
	if n < 0:
		return -n**2
	return n**2


class Joystick(connection.Client):
	def __init__(self):
		super().__init__()

		pygame.init()
		# surface = pygame.display.set_mode((400, 300), 0, 32)

		pygame.joystick.init()
		self.joysticks = []
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			print("Initialised: ", joystick.get_name())
			self.joysticks += [joystick]

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				2077,
				"rc_joy"
			]
		})

	def run(self):
		while True:
			self.loop()


	def loop(self):
		pygame.event.pump()
		# msg = input(">")
		# msg = "Cycle: " + str(i)
		# print("Sending: ", msg)
		# client.send_msg(bytearray(msg, 'utf-8'))

		position = {
			"axis": [self.joysticks[0].get_axis(i) for i in range(self.joysticks[0].get_numaxes())],
			"balls": [self.joysticks[0].get_ball(i) for i in range(self.joysticks[0].get_numballs())],
			"buttons": [self.joysticks[0].get_button(i) for i in range(self.joysticks[0].get_numbuttons())],
			"hats": [self.joysticks[0].get_hat(i) for i in range(self.joysticks[0].get_numhats())],
		}

		self.send_data({
			"type": "broadcast",
			"args": [
				{
					"type": "joy_position",
					"args": [
						position
					]
				},
				"rc_host"
			]
		})

		time.sleep(0.2)


if __name__ == '__main__':
	joy = Joystick()
	joy.start()
	joy.join()
