#testing phue and mqtt for motion sensing lights

import phue
import time
import random
import json
import pygame



deadzone = 0.25

def correctJoy(n):
	if n < deadzone and n > -deadzone:
		return 0.
	if n < 0:
		return -n**2
	return n**2

def run():
	b = phue.Bridge('192.168.1.211')
	b.connect()
	print(b.get_api())

	pygame.init()
	# surface = pygame.display.set_mode((400, 300), 0, 32)

	pygame.joystick.init()
	joysticks = []
	for i in range(pygame.joystick.get_count()):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
		print("Initialised: ", joystick.get_name())
		joysticks += [joystick]

	# light_names = b.get_light_objects('name')
	# light_names['cal'].colormode = 'hs'

	base = 0
	last = 0
	offset = 0
	button_hot = [False] * joysticks[0].get_numbuttons()


	i = 0
	while True:
		pygame.event.pump()

		temp = {
			"axis": [joysticks[0].get_axis(i) for i in range(joysticks[0].get_numaxes())],
			"balls": [joysticks[0].get_ball(i) for i in range(joysticks[0].get_numballs())],
			"buttons": [joysticks[0].get_button(i) for i in range(joysticks[0].get_numbuttons())],
			"hats": [joysticks[0].get_hat(i) for i in range(joysticks[0].get_numhats())],
		}

		for i in range(joysticks[0].get_numbuttons()):
			if temp["buttons"][i]:
				if not button_hot[i]:
					button_hot[i] = True
					if i == 0:
						base = random.uniform(0, 1)
					elif i == 1:
						last = (((1+temp["axis"][0]) / 2)+offset) % 1
			else:
				if button_hot[i]:
					button_hot[i] = False

		if button_hot[1]:
			offset = (last-((1+temp["axis"][0]) / 2)) % 1
		

		command = {
			'transitiontime': 1,
			'bri': int((1-((1+temp["axis"][2]) / 2)) * 254),
			'hue': int(((base+(((1+temp["axis"][0]) / 2)+offset)) % 1) * 65535),
			'sat': int((1-((1+temp["axis"][1]) / 2)) * 254)
		}

		print(temp)
		print(command)
		b.set_light('cal', command)

		time.sleep(0.1)
		i += 1


if __name__ == '__main__':
	run()