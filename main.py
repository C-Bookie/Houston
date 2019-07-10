# title: Show Host
# aurthor: Callum B-C

import yaml

import connection
import session


class Hand(session.Node):
	def __init__(s, conn, host=None):
		super().__init__(conn, host)


	def callback(s, socket_hook, data):
		if super().callback(socket_hook, data):
			answerSpace = connection.decode(data)
			session.dprint(str(answerSpace))

			if not s.responding:
				raise Exception("Unexpected response/unrecognised type: " + answerSpace["type"])
			s.session.response.put(answerSpace)
			s.responding = False

	def end(s, exception=False):  # todo review
		s.session.end()

class Show(session.Session):
	def __init__(s, manager, name):
		super().__init__(manager, name)


class ShowHost(session.SessionManager):
	def __init__(s, port=8089):
		super().__init__(port)

###

def run():
	shows = []

	# adding a show
	with open("shows.yaml", 'r') as showList:
		shows.append(Show(yaml.load(showList)["room1"]))


class Show():
	def __init__(self, showScript):
		self.script = showScript
		self.reset()

	# reset all IOs and states
	def reset(self):
		for node in self.script["panels"]:
			for feature in self.script["panels"][node]["out"]:
				if "default" in self.script["panels"]:
					pass  # todo send MQTT command, topic: "show/node", finger, self.script["panels"][node][finger]["default"]

	# reload a shows state from an SQL database that the show host will auto save to periodically
	def reload(self):
		pass

	# begin timer
	def start(self):
		pass


if __name__ == "__main__":
	run()