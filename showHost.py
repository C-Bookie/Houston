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
		s.script = None

	def load_script(s, room="room1"):
		with open("shows.yaml", 'r') as showList:
			s.script = yaml.load(showList)[room]

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


class ShowHost(session.SessionManager):
	def __init__(s, port=8089):
		super().__init__(port)
		s.node_hook = Hand
		s.session_hook = Show
		s.make_session("room1")

	def run(s):
		while True:
			conn, address = s.sock.accept()
			node = s.node_hook(conn, s)
			node.address = address  # todo review
			s.join_session(node, "room1")
			node.start()


if __name__ == "__main__":
	host = ShowHost()
	host.run()
