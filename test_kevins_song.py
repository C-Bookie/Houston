import pygame.midi
import connection


class Kevin(connection.Client): # Kevin plays the keyboard
	def __init__(self):
		super().__init__()
		self.white_list_functions += [
			"draw"
		]
		self.last_notes_down = set()


	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"graph",
				2077
			]
		})

	def draw(self, frame_rate, graph, graph1, sample, hsv, peaks, troughs):
		notes_down = set()
		for peak in peaks:
			notes_down.add(pygame.midi.frequency_to_midi(frame_rate * peak))

		for note in self.last_notes_down - notes_down:
			self.send_data({
				"type": "broadcast",
				"args": [
					{
						"type": "note",
						"args": [
							note,
							False

						]
					},
					"piano"
				]
			})

		for note in notes_down - self.last_notes_down:
			self.send_data({
				"type": "broadcast",
				"args": [
					{
						"type": "note",
						"args": [
							note,
							True

						]
					},
					"piano"
				]
			})

		self.last_notes_down = notes_down


if __name__ == "__main__":
	kevin = Kevin()
	kevin.run()
