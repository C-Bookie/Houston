import json
import socket
import struct
import threading

import serial

# TODO add heartbeat
# TODO make session client (rpc() connect())

DEBUG = True


def encode(data):
	def set_default(obj):
		if isinstance(obj, set):
			return list(obj)
		return obj
		# raise TypeError
	return json.dumps(data, default=set_default)


def decode(data):
	return json.loads(data)


class SocketHook(threading.Thread):
	closed = threading.Event()

	def __init__(self, conn, host=None):
		threading.Thread.__init__(self)
		self.conn = conn
		self.host = host
		self.closing = threading.Event()
		self.addr, self.port = self.conn.getpeername()
		self.setName("Connection-" + self.addr + ":" + str(self.port))
		self.debug_print("Connection opened")
		self.white_list_functions = []

	def debug_print(self, *args):
		if DEBUG:
			print(self.addr, '|', self.port, '\t', *args)

	def callback(self, msg):  # todo review
		response = decode(msg)
		if "type" in response and response["type"] in self.white_list_functions:
			function = getattr(self, response["type"])
			if response["args"] is None:
				function()
			else:
				function(*response["args"])
		else:
#			raise self.IllegalResponse("Request unrecognised by server: " + response["type"], response)  # fixme
			raise Exception("Request unrecognised by server: " + str(response))

	def run(self):
		try:
			while not self.closing.is_set():
				self.loop()
		finally:
			self.close()

	def loop(self):
		raw_data = self.recv_msg()
		if raw_data is not None:
			msg = raw_data.decode()
			if msg != '':
				self.debug_print("Received: ", msg)
				if self.callback is not None:
					self.callback(msg)  # fixme added self, may break
		else:
			self.debug_print("Connection died")
			self.close()


	def send_data(self, data):
		msg = encode(data)
		self.send_msg(msg)

	def send_msg(self, msg):
		try:
			if msg == '':
				print("Cannot send empty data!")
			else:
				self.debug_print("Sending: ", msg)
				if type(msg) is str:
					msg = bytearray(msg, 'utf-8')
				size = struct.pack('<I', len(msg))
				# size = (bytes)(len(msg))
				msg = size + msg
				self.conn.sendall(msg)
		except Exception as e:
			self.close()
			raise e

	def recv_msg(self):
		raw_msg_len = self.recv_all(4)
		if not raw_msg_len:
			return None
		msg_len = struct.unpack('<I', raw_msg_len)[0]
		# self.debug_print("Length: ", msg_len)
		return self.recv_all(msg_len)

	def recv_all(self, n):
		data = b''
		while len(data) < n:
			packet = self.conn.recv(n - len(data))
			# self.debug_print("Packet: ", packet)
			if not packet:
				return None  # EOF
			data += packet
		return data

	def close(self):
		if not self.closing.is_set():
			self.debug_print("Closing connection...")
			self.closing.set()
			if self.host is not None:
				self.host.close(self)
			# self.conn.close()
			self.conn.shutdown(socket.SHUT_WR)
			self.debug_print("Closed connection")

	def __del__(self):
		self.close()


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
			self.loop()

	def loop(self):
		conn, address = self.sock.accept()
		connection = SocketHook(conn, self)
		connection.callback = self.callback
		connection.address = address
		self.connections += [connection]
		connection.start()

	def broadcast(self, msg):
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
				print("Reconnecting...")
			except Exception as exc:
				raise exc  # fixme handel reconnection

	def on_fail(self):
		print("Connection lost")
		self.connect()


class SerialHook(threading.Thread):
	def __init__(self, port, baud_rate=9600, callback=None):
		threading.Thread.__init__(self)
		self.ser = serial.Serial(port, baud_rate)
		self.callback = callback
		self.closed = threading.Event()

	def run(self):
		try:
			while not self.closed.is_set():
				self.loop()
		except Exception as exc:
			raise exc
		finally:
			self.__del__()

	def loop(self):
		self.ser.inWaiting()
		data = self.ser.readline()
		if data is not None:
			data = data.decode()

			while len(data) > 0 and data[-1] in ['\r', '\n']:
				data = data[:-1]

			if len(data) == 0:
				print("Empty string")
			else:
				print("(", self.ser.port, ")\tReceived: ", data)
				if self.callback is not None:
					self.callback(data)
		else:
			print("\tEmpty data!")
			self.closed.set()  # todo replace with self.close()

	def send_msg(self, msg):
		print("(", self.ser.port, ")\tSending: ", msg)
		if type(msg) is str:
			msg = bytearray(msg, 'utf-8')
		try:
			self.ser.write(msg)
			self.ser.flush()
		except Exception as exc:
			self.__del__()
			raise exc

	def __del__(self):
		self.ser.close()
		print("Closed connection")


if __name__ == "__main__":
	host = Host()
	host.run()