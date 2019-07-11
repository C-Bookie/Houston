import threading
import queue

import connection


DEBUG = True
def dprint(msg):
	if DEBUG:
		print(str(threading.current_thread().getName()) + ": " + str(msg))


class Node(connection.SocketHook):
	def __init__(s, conn, host=None):
		super().__init__(conn, host)
		s.closeAll = threading.Event()
		s.closeAll.clear()
		s.session = None

	def send(s, data):
		s.send_msg(connection.encode(data))

	#returns if "all clear"
	def callback(s, socket_hook, data):
		answerSpace = connection.decode(data)
		dprint(str(answerSpace))

		if answerSpace["type"] == "stop":
			s.end()

		elif answerSpace["type"] == "close":
			s.close()

		elif answerSpace["type"] == "trip":
			s.end(True)
			raise Exception("godot triped up: " + answerSpace["trip"])

		elif answerSpace["type"] == "moveLobby":
			s.session.manager.move_lobby(s, answerSpace["moveLobby"])  # todo get player ID

		else:
			return True
		return False

	def end(s, exception=False):  # todo review
		s.session.end()

	def close(s):
		dprint("closing")
		s.closeAll.set()
		s.end()
		super().close()


class Session(threading.Thread):
	def __init__(s, manager, name):
		super().__init__()
		s.manager = manager
		s.name = name
		s.setName("Session-" + s.name)
		s.nodes = []
		s.response = queue.Queue()


	def add_node(s, node: Node):
		s.nodes += [node]

	def remove_node(s, node: Node):
		for i in range(len(s.nodes) - 1, -1, -1):
			if s.nodes[i] is node:
				del s.nodes[i]

	def close(s, node: Node=None):
		s.manager.close(node)


class SessionManager(connection.Host):
	def __init__(s, port=8089):
		super().__init__(port)
		s.node_hook = Node
		s.session_hook = Session
		s.sessions = {}

	def run(s):
		while True:
			conn, address = s.sock.accept()
			assert address not in s.sessions
			node = s.node_hook(conn, s)
			node.address = address  # todo review
			s.join_session(node, node.address)
			node.start()

	def make_session(s, name):
		s.sessions[name] = s.session_hook(s, name)

	def remove_session(s, name):
		del s.sessions[name]  # todo review

	def move_session(s, node: Node, session: Session):
		s.leave_session(node)
		s.join_session(node, session.name)

	def join_session(s, node: Node, des):
		if des not in s.sessions:
			s.sessions[des] = s.session_hook(s, des)
			s.sessions[des].start()
		s.sessions[des].add_node(node)
		node.session = s.sessions[des]

	def leave_session(s, node: Node):
		node.session.remove_node()
		if len(node.session.nodes) == 0:
			s.remove_session(node.session.name)  # todo review
		node.session = None

	def get_sessions(s):
		return s.sessions.keys()



