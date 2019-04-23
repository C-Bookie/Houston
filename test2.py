import connection
import time

if __name__ == "__main__":
	print("Host starting")
	host = connection.Host()
	host.start()
	print("Host started")

	while True:
		if len(host.connections) >= 1:
			msg = input(">")
			host.connections[-1].send_msg(bytearray(msg, 'utf-8'))
		else:
			time.sleep(1)
