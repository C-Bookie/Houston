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
		s.prop_list = []
		s.prop_status = {}

	def run(s):
		while not s.closeAll.is_set():
			response = s.response.get()
			# dprint("answer: " + str(answerSpace))

			if response["type"] == "new_node":
				if response["content"]["alias"] in s.prop_list:
					s.add_node(s.manager.unassigned[response["content"]["alias"]])
					del s.manager.unassigned[response["content"]["alias"]]


			else:
				raise Exception("Unrecognised type: " + response["type"])


class ShowHost(session.SessionManager):
	def __init__(s, show=Show, hand=Hand, port=8089):
		super().__init__(port)
		s.session_hook = Show
		s.node_hook = Hand
		s.unassigned = []

	def run(s):
		while True:
			conn, address = s.sock.accept()
			assert address not in s.sessions
			node = s.node_hook(conn, s)
			node.address = address  # todo review
			s.unassigned += [node]

			node.start()


if __name__ == "__main__":
	host = ShowHost()
	host.run()
