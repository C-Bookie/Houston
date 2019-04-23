import socket
import threading

import json
import struct
import time

global clientsocket

servo = 18
back = 22
forth = 23

trim = 85

class Client(threading.Thread):
    def __init__(self):
        super(Client, self).__init__()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('192.168.1.233', 8089))


    def run(self):
        while True:
            try:
                self.data = self.recv_msg().decode()
                if self.data != "":

                    print(self.data)

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
            print("error")
            #                if e.errno == errno.ECONNRESET:
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


if __name__ == '__main__':
    print("Client starting")
    client = Client()
    client.start()
    print("Client started")
    while True:
        msg = input(">")
        client.send_msg(bytearray(msg, 'utf-8'))




