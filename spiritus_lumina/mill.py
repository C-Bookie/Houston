import numpy as np

from caduceussocket import connection
from spiritus_lumina import jazZy


def callback(client, data):
	recived = connection.decode(data)
	result = client.host.lp.gen_slice(np.array(recived["sample"]), recived["frame_rate"])
	client.send_msg(connection.encode(result))

class JazzMill(connection.Host):
	def __init__(self):
		super().__init__()
		self.lp = jazZy.LightPlayer(None, False)
		self.callback = callback


if __name__ == "__main__":
	jm = JazzMill()
	jm.start()
	jm.join()

