import connection
import time

if __name__ == "__main__":
	host = connection.Host()
	host.start()

	while True:
		if len(host.connections) >= 1:
			msg = input(">")
			print("Sending: ", msg)
			host.connections[-1].send_msg(bytearray(msg, 'utf-8'))
		else:
			time.sleep(1)
