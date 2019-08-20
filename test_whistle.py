import math

import numpy as np
import matplotlib.pyplot as plt

import connection
import lights.jazZy


def sigmoid(x):
	return 1 / (1 + np.exp(-x))


class MidiWhistle(connection.Client):
	def __init__(self):
		super().__init__()

		# self.center = (0.1, 0.1, 0.2)

		self.velocity = 8  # lower is brighter
		self.curve = 3
		self.cap = 1.5
		# self.cutin = 0.0
		# self.cutoff = 1
		self.hueCo = (1 / 2)
		self.satCo = (1 / 5)
		self.briCo = (1 / 10)

		self.user_frame_rate = 15
		in_stream, input_info = lights.jazZy.openInputStream(None, self.user_frame_rate)
		stream_framerate = int(input_info["defaultSampleRate"])
		chunk_size = stream_framerate // self.user_frame_rate
		self.live_input_stream = lights.jazZy.LiveInputStream(in_stream, chunk_size)
		self.live_input_stream.start()

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"whistle",
				2077
			]
		})

	def loop(self):  # fixme don't override
		data = self.live_input_stream.queue.get()
		da = np.fromstring(data, dtype=np.int16)
		left, right = da[0::2], da[1::2]  # left and right channel
		sample = right
		frame_rate = self.user_frame_rate

		scaler = 10**self.velocity

		limit = scaler / frame_rate
		sample = sample / limit

		graph = np.abs(np.fft.rfft(sample).real) #** (1 / co)
		graph = np.array([x*y for x, y in zip(range(len(graph)), graph)])
		graph1 = sigmoid(graph) * 2 - 1
		graph1 **= self.curve

		min = 0
		# max = int(limit)
		max = int(len(graph1)/self.cap)

		l = max - min
		graph1 = graph1[min:max]

		points_x = []
		points_y = []
		for i in range(l):
			freq = graph1[i]
			theta = i / l
			theta **= self.hueCo
			# theta *= self.cutoff - self.cutin  # cuts pink from the rainbow
			# theta += self.cutin
			theta *= math.pi * 2
			points_x += [freq * math.sin(theta)]
			points_y += [freq * math.cos(theta)]

		x = np.sum(points_x) / len(points_x)
		y = np.sum(points_y) / len(points_y)

		hue = (math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)
		sat = math.sqrt((x * x) + (y * y))
		bri = sum(sigmoid(abs(sample)) * 2 - 1) / len(sample)

		sat **= self.satCo
		bri **= self.briCo

		self.send_data({
			"type": "broadcast",
			"args": [
				{
					"type": "draw",
					"args": [
						list(graph),
						list(graph1),
						list(sample),
						(hue, sat, bri)
					]
				},
				"graph"
			]
		})
		self.live_input_stream.queue.task_done()


if __name__ == "__main__":
	whistle = MidiWhistle()
	whistle.run()
