import serial

with serial.Serial('COM10', 9600) as ser:
	while True:
		reading = ser.readline().decode()
		print(reading)
		ser.write(bytearray(reading, 'utf-8'))

