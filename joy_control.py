#Object accounting for button presses
#Polled constantly

from shell_types import Pq_obj
from time import time
import pygame

# An object that parses joystick data, and supplies it to all functions in functsToCall
# Can print out this data if this object's print_joy_data is included
# Functions called should take three parameters:
# - axesData: contains four numbers in range (-1, 1): Front/back, left/right, yaw left/right, throttle up/down
# - hatData: a list of (int, int) tuples,
# - buttonData: a list of three lists:
#   - each button (number) that was pressed since the last update
#   - each button (number) that was released since the last update
#   - a list of all buttons, with '1' for pressed and '0' for released
class Joy_control:
	def __init__(self):
		self.functsToCall = []
		self.inQueue = False
		self.initialized = False
		self.time = time()

		self.arduinoWriteTime = time()

		pygame.init()

		# Initialize the joystick
		# Don't crash the whole program if we can't find a joystick
		try:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
			self.initialized = True
		except pygame.error:
			print("Cannot find joystick. Not running joystick.")
			return

		self.name = self.joystick.get_name()
		print(self.name)

		self.numaxes = self.joystick.get_numaxes()

		self.buttons = []
		self.numbuttons = self.joystick.get_numbuttons()
		for i in range(self.numbuttons):
			self.buttons.append(self.joystick.get_button(i))

		self.numhats = self.joystick.get_numhats()

	# A very quick function for ensuring the joystick data is constantly updated without backlogging
	def poll_function(self):
		# Prevents multiple of these objects in the queue
		if self.inQueue or not self.initialized:
			return None

		self.inQueue = True
		return [Pq_obj(3, self.event_function)]

	def add_function_to_call(self, function):
		self.functsToCall.append(function)

	# Reads the joystick data and runs all functions that are linked to this object
	def event_function(self):
		# Get a list of numbers from the current axis positions
		# Sign flip on all axis
		axes = [0 - self.joystick.get_axis(1), 0 - self.joystick.get_axis(0), 0 - self.joystick.get_axis(3),
				0 - self.joystick.get_axis(2)]

		# Read the data from all hat switches
		hatData = []
		for i in range(self.numhats):
			hatData.append(self.joystick.get_hat(i))

		# List off the buttons statuses. List both new presses, new releases, and a list of all button statuses
		buttonsPressed = []
		buttonsReleased = []
		buttonStatus = []
		for i in range(self.numbuttons):
			if self.joystick.get_button(i) == 1:
				buttonStatus.append(1)
				if self.buttons[i] == 0:
					self.buttons[i] = 1
					buttonsPressed.append(i)
			else:
				buttonStatus.append(0)
				if self.buttons[i] == 1:
					self.buttons[i] = 0
					buttonsReleased.append(i)

		# If you remove this line the code breaks. Don't ask me why
		for event in pygame.event.get(): ''''''

		for f in self.functsToCall:
			f(axes, hatData, [buttonsPressed, buttonsReleased, buttonStatus])

		self.inQueue = False

	# Prints out the joystick data
	def print_joy_data(self, axesData, hatData, buttonData):
		# Only print axis and hat positions each half second
		if time() - self.time > 0.5:
			self.time = time()
			print('Front/back: ' + str(axesData[0]) + '; Left/right: ' + str(axesData[1]), end='')
			print('; Yaw left/right: ' + str(axesData[2]) + '; Throttle up/down: ' + str(axesData[3]))
			print('Hat position x, y: ' + str(hatData[0][0]) + ', ' + str(hatData[0][1]))
		# Print out whenever buttons are pressed or released
		# Note that if we only printed this out every half second like the axes above, we'd need
		# to check each button's status instead of counting on the press/release lists
		for i in buttonData[0]:
			print("Button " + str(i) + " pressed.")
		for i in buttonData[1]:
			print("Button " + str(i) + " released.")
