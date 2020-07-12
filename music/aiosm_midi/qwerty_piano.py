import pygame
import pygame.midi

import mido

deadzone = 0.1


def correct_joy(n):
	if deadzone > n > -deadzone:
		return 0
	else:
		return n


# if n < 0:
# 	return -n**2
# return n**2


class JoyManager:
	def __init__(self, joystick):
		self.joystick = joystick
		self.joystick.init()

		self.axes = [correct_joy(self.joystick.get_axis(i)) for i in range(self.joystick.get_numaxes())]
		self.balls = [self.joystick.get_ball(i) for i in range(self.joystick.get_numballs())]
		self.buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
		self.hats = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

		self.total_offset = len(self.buttons) + len(self.hats)


mapping = {
	pygame.K_BACKQUOTE: 29,  # F1
	pygame.K_1: 31,  # G1
	pygame.K_2: 33,  # A1
	pygame.K_3: 35,  # B1
	pygame.K_4: 36,  # C2
	pygame.K_5: 38,  # D2
	pygame.K_6: 40,  # E2
	pygame.K_7: 41,  # F2
	pygame.K_8: 43,  # G2
	pygame.K_9: 45,  # A2
	pygame.K_0: 47,  # B2
	pygame.K_MINUS: 48,  # C3
	pygame.K_EQUALS: 50,  # D3

	pygame.K_q: 43,  # G2
	pygame.K_w: 45,  # A2
	pygame.K_e: 47,  # B2
	pygame.K_r: 48,  # C3
	pygame.K_t: 50,  # D3
	pygame.K_y: 52,  # E3
	pygame.K_u: 53,  # F3
	pygame.K_i: 55,  # G3
	pygame.K_o: 57,  # A3
	pygame.K_p: 59,  # B3
	pygame.K_LEFTBRACKET: 60,  # C4
	pygame.K_RIGHTBRACKET: 62,  # D4

	pygame.K_a: 55,  # G3
	pygame.K_s: 57,  # A3
	pygame.K_d: 59,  # B3
	pygame.K_f: 60,  # C4
	pygame.K_g: 62,  # D4
	pygame.K_h: 64,  # E4
	pygame.K_j: 65,  # F4
	pygame.K_k: 67,  # G4
	pygame.K_l: 69,  # A4
	pygame.K_SEMICOLON: 71,  # B4
	pygame.K_QUOTE: 72,  # C5
	92: 74,  # D5  HASH

	60: 65,  # F4  BACKSLASH
	pygame.K_z: 67,  # G4
	pygame.K_x: 69,  # A4
	pygame.K_c: 71,  # B4
	pygame.K_v: 72,  # C5
	pygame.K_b: 74,  # D5
	pygame.K_n: 76,  # E5
	pygame.K_m: 77,  # F5
	pygame.K_COMMA: 79,  # G5
	pygame.K_PERIOD: 81,  # A5
	pygame.K_SLASH: 83  # B5
}


class QwertyPiano:
	def __init__(self):
		self.step_up = 0

		self.height = 300
		self.width = 400

		pygame.init()

		self.joysticks = [JoyManager(pygame.joystick.Joystick(i)) for i in range(pygame.joystick.get_count())]

		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('jazZy')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

	def get_messages(self):
		for event in pygame.event.get():  # may need pump=True
			msg = None
			if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
				if event.key in mapping:
					if event.type == pygame.KEYDOWN:
						msg = mido.Message('note_on', note=mapping[event.key])
					else:
						msg = mido.Message('note_off', note=mapping[event.key])
				elif event.key == pygame.K_SPACE:
					value = 127 if event.type == pygame.KEYDOWN else 0
					msg = mido.Message('control_change', control=64, value=value)

			elif event.type == pygame.JOYAXISMOTION:
				value = int((correct_joy(event.value) + 1) / 2 * 127)
				if self.joysticks[event.joy].axes[event.axis] != value:
					self.joysticks[event.joy].axes[event.axis] = value
					axis_offset = sum([len(joystick.axes) for joystick in self.joysticks]) + event.axis
					msg = mido.Message('control_change', control=axis_offset + 32, value=value)
			# elif event.type == pygame.JOYBALLMOTION:
			# 	pass

			elif event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
				button_down = event.type == pygame.JOYBUTTONDOWN
				self.joysticks[event.joy].buttons[event.button] = button_down
				offset = sum([joystick.total_offset for joystick in self.joysticks[:event.joy]]) \
						 + event.button
				msg = mido.Message('note_on' if button_down else 'note_off', note=offset + 60)

			elif event.type == pygame.JOYHATMOTION:
				button_down = sum([abs(n) for n in event.value]) != 0
				offset = sum([joystick.total_offset for joystick in self.joysticks[:event.joy]])
				offset += len(self.joysticks[event.joy].buttons) + event.hat
				msg = mido.Message('note_on' if button_down else 'note_off', note=offset + 60)

			elif event.type == pygame.QUIT:
				yield None

			if msg is None:
				continue
			else:
				yield msg

		self.screen.blit(self.background, (0, 0))
		pygame.display.update()


