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


	def run(s):
		while not s.closeAll.is_set():
			answerSpace = s.response.get()
			# dprint("answer: " + str(answerSpace))

			if answerSpace["type"] == "entryList":
				s.begin(answerSpace["entryList"])
				s.GI.setName("GameInstance-" + s.name)
				i = 0
				for player in s.nodes:
					while answerSpace["entryList"]["players"][i]["MPID"] < 0:
						i += 1
					player.ID = answerSpace["entryList"]["players"][i]["MPID"]
					i += 1

			elif answerSpace["type"] == "answer":
				if answerSpace["answer"] is None:
					s.toPython.put(list())
				else:
					s.toPython.put(answerSpace["answer"])

			elif answerSpace["type"] == "pass_question":
				s.toPython.put(s.auto_answer(answerSpace["pass_question"]))

			else:
				raise Exception("Unrecognised type: " + answerSpace["type"])


class ShowHost(session.SessionManager):
	def __init__(s, show=Show, hand=Hand, port=8089):
		super().__init__(port)
		s.session_hook = Show
		s.node_hook = Hand
		s.make_session("room1")



if __name__ == "__main__":
	host = ShowHost()
	host.run()
