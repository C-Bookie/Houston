import json

import connection
import time


def reciever(data):
	data = json.loads(data)
	x = data["axis"][0]
	y = -data["axis"][1]
	left = 1
	right = 1

	if x < 0:
		left -= abs(x)
	else:
		right -= x


	left *= y
	right *= y
	left *= 1023
	right *= 1023
	left = (int)(left)
	right = (int)(right)

	msg = str(left)+'|'+str(right)+'\n'
	# arduino.sendMsg(msg)
	print(msg)

if __name__ == "__main__":
	host = connection.Host(callback=reciever)
	host.start()

	# arduino = connection.SerialHook('COM12', 9600)
	# arduino.ser.flushInput()
	# arduino.ser.flushOutput()
	# arduino.start()

	while True:
			time.sleep(1)
