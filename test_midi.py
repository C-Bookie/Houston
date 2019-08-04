
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
	step_up = 30

	mapping = {
		pygame.K_q: 0,
		pygame.K_w: 1,
		pygame.K_e: 2,
		pygame.K_r: 3,
		pygame.K_t: 4,
		pygame.K_y: 5,
		pygame.K_u: 6,
		pygame.K_i: 7,
		pygame.K_o: 8,
		pygame.K_p: 9,
		pygame.K_a: 10,
		pygame.K_s: 11,
		pygame.K_d: 12,
		pygame.K_f: 13,
		pygame.K_g: 14,
		pygame.K_h: 15,
		pygame.K_j: 16,
		pygame.K_k: 17,
		pygame.K_l: 18,
		pygame.K_z: 19,
		pygame.K_x: 20,
		pygame.K_c: 21,
		pygame.K_v: 22,
		pygame.K_b: 23,
		pygame.K_n: 24,
		pygame.K_m: 25
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
					note = s.mapping[event.key] + s.step_up
					s.send_note(note, True)
				if event.type == pygame.KEYUP:
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
