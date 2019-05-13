import json

import connection

if __name__ == '__main__':
	client = connection.Client()
	client.start()

	data = {
		"sensor": "gps",
		"time": 1351824120,
		"data": [
			48.756080,
			2.302038
		]
	}

	while True:
		input(">")
		if client.closed.is_set():
			break
		msg = json.dumps(data)
		client.send_msg(msg)
