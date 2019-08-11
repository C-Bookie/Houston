
#todo wistle to midi, get audio stream and convert frequency to note, activate based on volume
#todo sine wave modulation generator

import pygame
import mido

import pygame.midi

def test1():
	mid1 = mido.MidiFile('midi/sample1-1.mid')
	mid2 = mido.MidiFile('midi/sample1-2.mid')

	assert len(mid1.tracks[0]) == len(mid2.tracks[0])

	for i in range(len(mid1.tracks[0])):
		if not mid1.tracks[0][i].is_meta:
			mid1.tracks[0][i].time = mid2.tracks[0][i].time

	mid1.save('midi/sample1-3.mid')


class Piano():
	step_up = 0

	mapping = {
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

	height = 300
	width = 400

	pygame.init()
	screen = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
	pygame.display.set_caption('jazZy')

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

#	print(mido.get_output_names())
	port = mido.open_output("moo 1")

	def run(s):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						msg = mido.Message("control_change", control=64, value=127)
						s.port.send(msg)
						print("Sustain Down")
					elif event.key in s.mapping:
						note = s.mapping[event.key] + s.step_up
						s.send_note(note, True)
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						msg = mido.Message("control_change", control=64, value=0)
						s.port.send(msg)
						print("Sustain Up")
					elif event.key in s.mapping:
						note = s.mapping[event.key] + s.step_up
						s.send_note(note, False)
				if event.type == pygame.QUIT:
					return

			s.screen.blit(s.background, (0, 0))
			pygame.display.flip()

	def send_note(s, note, on):
		command = 'note_on' if on else 'note_off'
		msg = mido.Message(command, note=note)
		s.port.send(msg)
		print(pygame.midi.midi_to_ansi_note(note) + ": " + command)

def test2():
	piano = Piano()
	piano.run()

if __name__ == "__main__":
	test2()
