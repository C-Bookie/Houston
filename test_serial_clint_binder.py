from time import sleep
import connection

if __name__ == "__main__":
	arduino = connection.SerialHook('COM12', 9600)
	client = connection.Client(callback=arduino.send_msg)
	arduino.callback = client.send_msg
	arduino.start()
	client.start()

	while True:
		sleep(1)


