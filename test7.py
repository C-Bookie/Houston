import json

import connection
import time

import pygame

deadzone = 0.25

def correctJoy(n):
	if n < deadzone and n > -deadzone:
		return 0.
	if n < 0:
		return -n**2
	return n**2

if __name__ == '__main__':

	pygame.init()
	# surface = pygame.display.set_mode((400, 300), 0, 32)

	pygame.joystick.init()
	joysticks = []
	for i in range(pygame.joystick.get_count()):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
		print("Initialised: ", joystick.get_name())
		joysticks += [joystick]

	client = connection.Client()
	client.start()

	i = 0
	while True:
		pygame.event.pump()
		# msg = input(">")
		# msg = "Cycle: " + str(i)
		# print("Sending: ", msg)
		# client.send_msg(bytearray(msg, 'utf-8'))

		temp = {
			"axis": [joysticks[0].get_axis(i) for i in range(joysticks[0].get_numaxes())],
			# "balls": [joysticks[0].get_ball(i) for i in range(joysticks[0].get_numballs())],
			# "buttons": [joysticks[0].get_button(i) for i in range(joysticks[0].get_numbuttons())],
			# "hats": [joysticks[0].get_hat(i) for i in range(joysticks[0].get_numhats())],
		}
		print(temp)
		msg = json.dumps(temp)
		client.send_msg(msg)

		time.sleep(0.1)
		i += 1
