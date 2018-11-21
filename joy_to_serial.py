from time import time
import serial


class Arduino_arm_control:
	def __init__(self):
		self.time = time()

		# Try to open a
		self.portsToTry = ['COM3', 'COM5', 'COM4', '/dev/ttyUSB0', '/dev/ttyUSB1',
							'/dev/ttyAMA0', '/dev/ttyAMA1', '/dev/ttyACM0', '/dev/ttyACM1']

		self.ser = None
		for port in self.portsToTry:
			try:
				self.ser = serial.Serial(port, 9600)
				print("Serial opened on port " + port)
				break
			except:
				print("error on serial " + port)

	def write_to_arduino(self, axesData, hatData, buttonData):
		# Ensure we have the port.
		if not self.ser:
			return

		# Ensure we don't overwhelm the serial (or stall main program)
		if time() - self.time < 0.05:
			return

		self.time = time()

		# Mapped from -100 to 100, with positive being forward, negative being backward
		# Bad simple for byte encoding. Fix this to be centered on 0
		lowerSpeed = int(axesData[0] * 100)

		# Create a small dead zone
		if lowerSpeed < 5 and lowerSpeed > -5:
			lowerSpeed = 0

		# This will be -50, 0, or 50. We don't have an axis for this one.
		upperSpeed = hatData[0][1] * 50

		# print(lowerSpeed, end=' ')
		# print(upperSpeed)

		self.ser.write(bytes(str(lowerSpeed) + ' ', encoding="ascii"))
		self.ser.write(bytes(str(upperSpeed) + " ", encoding="ascii"))
		self.ser.write(bytes(str(314) + "\n", encoding="ascii"))
