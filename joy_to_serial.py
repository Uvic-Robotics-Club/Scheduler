from time import time
import serial
import random

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

	def write_to_arm(self, axesData, hatData, buttonData):
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

		rotateSpeed = int(axesData[2] * 10)

		self.ser.write(bytes(str(lowerSpeed) + ' ', encoding="ascii"))
		self.ser.write(bytes(str(upperSpeed) + " ", encoding="ascii"))
		self.ser.write(bytes(str(rotateSpeed) + " ", encoding="ascii"))
		self.ser.write(bytes(str(314) + "\n", encoding="ascii"))

	# This function does all the calculations to turn joystick input into drive motor output.
	def print_power(self, axesData, hatData, buttonData):

		# power_array's indices represent the four wheels as follows:
		# 0 1
		# 2 3
		# (0 and 1 being the front wheels of the rover, and 0 and 2 being the left wheels of the rover, as viewed from a bird's-eye view.)
		power_array = [0, 0, 0, 0]

		# If the joystick is centred, engage swivel mode
		# Note that the constants to engage "swivel mode" also create a dead zone
		if abs(axesData[0]) < 0.14 and abs(axesData[1]) < 0.14:
			if abs(axesData[2]) > 0.2:
				power_array = [-axesData[2], -axesData[2], -axesData[2], -axesData[2]]

		# Else, calculate motor power levels
		else:
			# First, set all four wheels at the same power level according to the forward/back tilt
			power_array = [axesData[0], -axesData[0], axesData[0], -axesData[0]]
			# Next, cut power from either side of the rover according to left/right joystick tilt
			# left tilt is positive; right is negative
			if axesData[1] > 0:
				power_array[0] = power_array[0] * (1-axesData[1])
				power_array[2] = power_array[2] * (1-axesData[1])
			else:
				power_array[1] = power_array[1] * (1+axesData[1])
				power_array[3] = power_array[3] * (1+axesData[1])


		# Scale the output based on the throttle
		# Scales from 10% to 100% of max power
		power_array = [i*(axesData[3]*45+55) for i in power_array]

		# When we actually start using my algorithm, we'll get this sent to the motors instead of just being printed. For now, we print for demonstration purposes.
		print("FINAL POWER ARRAY: ")
		print(power_array[0], power_array[1])
		print(power_array[2], power_array[3])


