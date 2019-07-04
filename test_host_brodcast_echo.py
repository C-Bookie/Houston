import time
import connection


if __name__ == "__main__":
	host = connection.Host()
	host.callback = host.boradcast
	host.start()

	while True:
			time.sleep(1)

