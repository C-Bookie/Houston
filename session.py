import random
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
		s.alias = s.addr + ":" + str(s.port)

	def send(s, data):
		s.send_msg(connection.encode(data))

	#returns if "all clear"
	def callback(s, data):
		answerSpace = connection.decode(data)
		dprint(str(answerSpace))

		if answerSpace["type"] == "close":
			s.close()

		elif answerSpace["type"] == "stop":
			s.session.end()

		elif answerSpace["type"] == "trip":
			s.session.end(True)
			raise Exception("godot triped up: " + answerSpace["trip"])

		elif answerSpace["type"] == "move_session":
			s.session.manager.move_session(s, str(answerSpace["content"]))  # todo get player ID

		elif answerSpace["type"] == "get_sessions":
			s.send({
				"type": "session_list",
				"content": s.session.manager.get_sessions()
			})

		elif answerSpace["type"] == "broadcast":
			s.session.broadcast(answerSpace)

		else:
			return True
		return False

	def close(s):
		dprint("closing")
		s.closeAll.set()
		s.session.end()
		super().close()


class Session(threading.Thread):
	def __init__(s, manager, alias):
		super().__init__()
		s.manager = manager
		s.setName("Session-" + alias)
		s.alias = alias
		s.nodes = []
		s.response = queue.Queue()

	def broadcast(s, data):
		for node in s.nodes:
			node.send(data)

	def add_node(s, node: Node):
		s.nodes += [node]
		dprint("Added node: " + node.alias + " -> " + s.alias)

	def remove_node(s, node: Node):
		for i in range(len(s.nodes) - 1, -1, -1):
			if s.nodes[i] is node:
				del s.nodes[i]
				dprint("Removed node: " + node.alias + " <- " + s.alias)

	# def close(s, node: Node=None):
	# 	s.manager.close(node)

	def end(s, exception=False):
		pass


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
			alias = str(random.randint(1<<8, 1<<16))
			s.join_session(node, alias)  # fixme unique room ID's needed
			node.start()

	def move_session(s, node: Node, des):
		dprint("Moving node: " + node.alias + " -> " + des)
		s.leave_session(node)
		s.join_session(node, des)

	def join_session(s, node: Node, des):
		if des not in s.sessions:
			s.sessions[des] = s.session_hook(s, des)
			s.sessions[des].start()
			dprint("Created new session: " + des)
		s.sessions[des].add_node(node)
		node.session = s.sessions[des]

	def leave_session(s, node: Node):
		node.session.remove_node(node)
		if len(node.session.nodes) == 0:
			del s.sessions[node.session.alias]  # todo review
			dprint("Deleted old session: " + node.session.alias)
		node.session = None

	def get_sessions(s):
		return s.sessions.keys()

	# def close(s, node: Node=None):  # todo rename to leave_lobby()
	# 	if node is not None:  # fixme deal with else
	# 		node.session.remove_node(node)
	# 		if len(node.session.nodes) == 0:
	# 			del s.sessions[node.session.alias]
	# 		del node


