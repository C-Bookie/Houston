import json
import socket
import struct
import threading

import serial

DEBUG = False

class SocketHook(threading.Thread):
	def __init__(self, conn, callback=None):
		threading.Thread.__init__(self)
		self.conn = conn
		self.callback = callback
		self.data = ""
		self.addr, self.port = self.conn.getpeername()
		self.setName("Thread-" + self.addr + ":" + str(self.port))
		print(self.conn.getpeername(), "\tConnection opened")


	def run(self):
		try:
			while True:
				self.data = self.recv_msg()
				if self.data is not None:
					self.data = self.data.decode()
					if self.data != '':
						print(self.conn.getpeername(), "\tRecieved: ", self.data)
						if self.callback is not None:
							self.callback(self.data)
				else:
					print(self.conn.getpeername(), "\tEmpty data!")
					break
		# except socket.error as e:
			# if e.errno == errno.ECONNRESET:
		except Exception as e:
			raise(e)
		finally:
			self.__del__()

	def send_msg(self, msg):
		if msg == '':
			print("Cannot send empty data!")
		else:
			try:
				if type(msg) is str:
					msg = bytearray(msg, 'utf-8')
				size = struct.pack('>I', len(msg))
				# size = (bytes)(len(msg))
				msg = size + msg
				self.conn.sendall(msg)
			except Exception as e:
				self.__del__()
				raise(e)

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
		if DEBUG:
			print(self.conn.getpeername(), "\tLength: ", msglen)
		return self.recvall(msglen)

	def recvall(self, n):
		# Helper function to recv n bytes or return None if EOF is hit
		data = b''
		while len(data) < n:
			packet = self.conn.recv(n - len(data))
			if DEBUG:
				print(self.conn.getpeername(), "\tPacket: ", packet)
			if not packet:
				return None
			data += packet
		return data

	def __del__(self):
		print(self.conn.getpeername(), "\tClosing connection...")
		# self.conn.detach()
		# self.conn.shutdown(socket.SHUT_RDWR)
		self.conn.close()
		print("Closed connection")

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
			connection = SocketHook(conn, self.callback)
			connection.address = address
			self.connections += [connection]
			connection.start()

class Client(SocketHook):
	def __init__(self, ip='127.0.0.1', port=8089, callback=None):
		print("Client starting...")
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((ip, port))
		print("Client started: ", conn.getsockname())
		super(Client, self).__init__(conn, callback)


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
			raise(e)
		finally:
			self.__del__()

	def sendMsg(self, msg):
		print("(", self.ser.port, ")\tSending: ", msg)
		if type(msg) is str:
			msg = bytearray(msg, 'utf-8')
		try:
			self.ser.write(msg)
		except Exception as e:
			self.__del__()
			raise(e)

	def __del__(self):
		self.ser.close()
		print("Closed connection")
