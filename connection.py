import json
import socket
import struct
import threading


class Connection(threading.Thread):
	def __init__(self, conn, callback=print):
		threading.Thread.__init__(self)
		self.conn = conn
		self.callback = callback
		self.data = ""


	def run(self):
		while True:
			try:
				self.data = self.recv_msg().decode()
				if self.data != "":
					self.callback(self.data)
				else:
					print("Empty data!")
			except socket.error as e:
				# if e.errno == errno.ECONNRESET:
				self.conn.close()
				break
			except Exception as e:
				raise (e)

	def send_msg(self, msg):
		try:
			msg = struct.pack('>I', len(msg)) + msg
			self.conn.sendall(msg)
		except socket.error as e:
			print("disconnected")
			# if e.errno == errno.ECONNRESET:
			self.conn.close()
			global loop
			loop = False

	def send_set(self, s):
		def set_default(obj):
			if isinstance(obj, set):
				return list(obj)
			raise TypeError

		data = json.dumps(s, default=set_default)
		self.send_msg(data.encode())

	def recv_msg(self):
		# Read message length and unpack it into an integer
		raw_msglen = self.recvall(4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return self.recvall(msglen)

	def recvall(self, n):
		# Helper function to recv n bytes or return None if EOF is hit
		data = b''
		while len(data) < n:
			packet = self.conn.recv(n - len(data))
			if not packet:
				return None
			data += packet
		return data

class Host(threading.Thread):
	def __init__(self):
		super(Host, self).__init__()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind(('', 8089))
		self.s.listen(5)  # become a server socket, maximum 5 connections
		self.connections = []

	def run(self):
		while True:
			conn, address = self.s.accept()
			connection = Connection(conn)
			self.connections += [connection]
			connection.start()
			print("New connection: ", len(self.connections))

class Client(Connection):
	def __init__(self, ip='127.0.0.1', port=8089):
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((ip, port))
		super(Client, self).__init__(conn)

