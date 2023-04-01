
#todo wistle to midi, get audio stream and convert frequency to note, activate based on volume
#todo sine wave modulation generator
import pygame
import mido
import pygame.midi

from music import midi_out
from caduceussocket import connection


def test1():
	mid1 = mido.MidiFile('../midi/sample1-1.mid')
	mid2 = mido.MidiFile('../midi/sample1-2.mid')

	assert len(mid1.tracks[0]) == len(mid2.tracks[0])

	for i in range(len(mid1.tracks[0])):
		if not mid1.tracks[0][i].is_meta:
			mid1.tracks[0][i].time = mid2.tracks[0][i].time

	mid1.save('midi/sample1-3.mid')


class MidiKeyboard(connection.Client):
	def __init__(self):
		super().__init__()
		self.step_up = 0

		self.mapping = {
			pygame.K_BACKQUOTE: 29,		# F1
			pygame.K_1: 31,				# G1
			pygame.K_2: 33,				# A1
			pygame.K_3: 35,				# B1
			pygame.K_4: 36,				# C2
			pygame.K_5: 38,				# D2
			pygame.K_6: 40,				# E2
			pygame.K_7: 41,				# F2
			pygame.K_8: 43,				# G2
			pygame.K_9: 45,				# A2
			pygame.K_0: 47,				# B2
			pygame.K_MINUS: 48,			# C3
			pygame.K_EQUALS: 50,		# D3

			pygame.K_q: 43,				# G2
			pygame.K_w: 45,				# A2
			pygame.K_e: 47,				# B2
			pygame.K_r: 48,				# C3
			pygame.K_t: 50,				# D3
			pygame.K_y: 52,				# E3
			pygame.K_u: 53,				# F3
			pygame.K_i: 55,				# G3
			pygame.K_o: 57,				# A3
			pygame.K_p: 59,				# B3
			pygame.K_LEFTBRACKET: 60,	# C4
			pygame.K_RIGHTBRACKET: 62,	# D4

			pygame.K_a: 55,				# G3
			pygame.K_s: 57,				# A3
			pygame.K_d: 59,				# B3
			pygame.K_f: 60,				# C4
			pygame.K_g: 62,				# D4
			pygame.K_h: 64,				# E4
			pygame.K_j: 65,				# F4
			pygame.K_k: 67,				# G4
			pygame.K_l: 69,				# A4
			pygame.K_SEMICOLON: 71,		# B4
			pygame.K_QUOTE: 72,			# C5
			92: 74,						# D5  HASH

			60: 65,						# F4  BACKSLASH
			pygame.K_z: 67,				# G4
			pygame.K_x: 69,				# A4
			pygame.K_c: 71,				# B4
			pygame.K_v: 72,				# C5
			pygame.K_b: 74,				# D5
			pygame.K_n: 76,				# E5
			pygame.K_m: 77,				# F5
			pygame.K_COMMA: 79,			# G5
			pygame.K_PERIOD: 81,		# A5
			pygame.K_SLASH: 83			# B5
		}

		self.height = 300
		self.width = 400

		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('jazZy')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"keyboard",
				2077
			]
		})

	def loop(self):
		events = pygame.event.get()
		for event in events:
			if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
				if event.key == pygame.K_SPACE:
					self.send_data({
						"type": "broadcast",
						"args": [
							{
								"type": "sustain",
								"args": [
									event.type == pygame.KEYDOWN
								]
							},
							"piano"
						]
					})
				elif event.key in self.mapping:
					self.send_data({
						"type": "broadcast",
						"args": [
							{
								"type": "note",
								"args": [
									self.mapping[event.key] + self.step_up,
									event.type == pygame.KEYDOWN
								]
							},
							"piano"
						]
					})
			if event.type == pygame.QUIT:
				return

		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()


if __name__ == "__main__":
	piano = midi_out.Piano()
	piano.start()
	keyboard = MidiKeyboard()
	keyboard.run()
