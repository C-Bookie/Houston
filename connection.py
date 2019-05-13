import json
import socket
import struct
import threading

import serial

DEBUG = True


class SocketHook(threading.Thread):
	closed = threading.Event()
	def __init__(self, conn, callback=None, host=None):
		threading.Thread.__init__(self)
		self.conn = conn
		self.callback = callback
		self.host = host
		self.closed = threading.Event()
		self.addr, self.port = self.conn.getpeername()
		self.setName("Thread-" + self.addr + ":" + str(self.port))
		self.debugPrint("Connection opened")

	def debugPrint(self, *args):
		if DEBUG:
			print(self.addr, '|', self.port, '\t', *args)

	def run(self):
		while not self.closed.is_set():
			try:
				data = self.recv_msg()
				if data is not None:
					data = data.decode()
					if data != '':
						self.debugPrint("Recieved: ", data)
						if self.callback is not None:
							self.callback(data)
				else:
					self.debugPrint("Empty data!")
					break
			except ConnectionResetError as e:
				# print(e.)
				self.onFail()
			except Exception as e:
				raise (e)

	def onFail(self):
		self.close()

	def send_msg(self, msg):
		try:
			if msg == '':
				print("Cannot send empty data!")
			else:
				self.debugPrint("Sending: ", msg)
				if type(msg) is str:
					msg = bytearray(msg, 'utf-8')
				size = struct.pack('>I', len(msg))
				# size = (bytes)(len(msg))
				msg = size + msg
				self.conn.sendall(msg)
		except Exception as e:
			self.close()
			raise (e)

	# def send_set(self, s):
	# 	def set_default(obj):
	# 		if isinstance(obj, set):
	# 			return list(obj)
	# 		raise TypeError
	#
	# 	data = json.dumps(s, default=set_default)
	# 	self.send_msg(data.encode())

	def recv_msg(self):
		raw_msglen = self.recvall(4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# self.debugPrint("Length: ", msglen)
		return self.recvall(msglen)

	def recvall(self, n):
		data = b''
		while len(data) < n:
			packet = self.conn.recv(n - len(data))
			# self.debugPrint("Packet: ", packet)
			if not packet:
				return None  # EOF
			data += packet
		return data

	def close(self):
		self.debugPrint("Closing connection...")
		self.closed.set()
		if self.host is not None:
			self.host.close(self)
		# self.conn.detach()
		# self.conn.shutdown(socket.SHUT_RDWR)
		self.conn.close()
		self.debugPrint("Closed connection")


class Host(threading.Thread):
	def __init__(self, port=8089, callback=None):
		print("Host starting...")
		super(Host, self).__init__()
		self.callback = callback
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', port))
		self.sock.listen(5)  # become a server socket, maximum 5 connections
		self.connections = []
		print("Host started: ", self.sock.getsockname())

	def run(self):
		while True:
			conn, address = self.sock.accept()
			connection = SocketHook(conn, self.callback, self)
			connection.address = address
			self.connections += [connection]
			connection.start()

	def boradcast(self, msg):
		for conn in self.connections:
			conn.send_msg(msg)

	def close(self, client):
		for i in range(len(self.connections)-1, -1, -1):
			if self.connections[i] is client:
				del self.connections[i]


class Client(SocketHook):
	def __init__(self, addr='127.0.0.1', port=8089, callback=None):
		self.addr = addr
		self.port = port
		print("Client starting...")
		self.connect()
		super(Client, self).__init__(self.conn, callback)
		print("Client started: ", self.conn.getsockname())

	def connect(self):
		print("Connecting")
		while not self.closed.is_set():
			try:
				self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.conn.connect((self.addr, self.port))
				print("Connected")
				break
			except ConnectionRefusedError:
				print("Reconecting...")
			except Exception as e:
				raise e  # fixme handel reconection

	def onFail(self):
		print("Connection lost")
		self.connect()


class SerialHook(threading.Thread):
	def __init__(self, port, bandrate=9600, callback=None):
		threading.Thread.__init__(self)
		self.ser = serial.Serial(port, bandrate)
		self.callback = callback

	def run(self):
		try:
			while True:
				self.ser.inWaiting()
				self.data = self.ser.readline()
				if self.data is not None:
					try:
						self.data = self.data.decode()
					except UnicodeDecodeError:
						continue

					while len(self.data) > 0 and self.data[-1] in ['\r', '\n']:
						self.data = self.data[:-1]

					if len(self.data) == 0:
						print("Empty string")
					else:
						print("(", self.ser.port, ")\tRecieved: ", self.data)
						if self.callback is not None:
							self.callback(self.data)
				else:
					print("\tEmpty data!")
					break
		except Exception as e:
			raise (e)
		finally:
			self.__del__()

	def sendMsg(self, msg):
		print("(", self.ser.port, ")\tSending: ", msg)
		if type(msg) is str:
			msg = bytearray(msg, 'utf-8')
		try:
			self.ser.write(msg)
			self.ser.flush()
		except Exception as e:
			self.__del__()
			raise (e)

	def __del__(self):
		self.ser.close()
		print("Closed connection")
