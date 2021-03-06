from caduceussocket import connection


class RCController(connection.Client):
	def __init__(self):
		super().__init__()

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

	def joy_position(self, data):
		x = data["axis"][0]
		y = -data["axis"][1]
		left = 1
		right = 1

		if x < 0:
			left -= abs(x)
		else:
			right -= x

		left *= y
		right *= y
		left *= 1023
		right *= 1023
		left = (int)(left)
		right = (int)(right)

		command = str(left)+'|'+str(right)+'\n'

		self.send_data({
			"type": "broadcast",
			"args": [
				command,
				"rc_car"
			]
		})


if __name__ == "__main__":
	host = RCController()
	host.start()
	host.join()
