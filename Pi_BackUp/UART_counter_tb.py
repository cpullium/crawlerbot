import pyserial

ser = serial.Serial('/dev/ttyAMA0', baudrate=9600)
x = '0'

while 1:
	ser.write(x+1)
	ser.flushOutput()
	while not ser.in_waiting
	x = ser.read(1)
	ser.flushInput()
	print x
