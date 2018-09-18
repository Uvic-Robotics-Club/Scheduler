#Object accounting for button presses
#Polled constantly

from shell_types import Pq_obj
from time import time
import pygame

class Joy_control:
	def __init__(self, val):
		self.inQueue = False
		self.val = val
		self.time = time()

		self.arduinoWriteTime = time()

		pygame.init()

		# Initialize the joystick
		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()

		self.name = self.joystick.get_name()
		print(self.name)

		self.numaxes = self.joystick.get_numaxes()
		print("{} axes".format(self.numaxes))

		self.buttons = []
		self.numbuttons = self.joystick.get_numbuttons()
		print("{} buttons".format(self.numbuttons))
		for i in range(self.numbuttons):
			self.buttons.append(self.joystick.get_button(i))

		self.numhats = self.joystick.get_numhats()
		print("{} hats".format(self.numhats))

	def poll_function(self):
		# Prevents multiple of these objects in the queue
		if self.inQueue:
			return None

		self.inQueue = True
		return Pq_obj(3, self.event_function)

	# Prints out thread
	def event_function(self):
		# Write commands to arduino
		self.write_to_arduino()

		# The joystick and hat positions are only printed periodically
		if time() - self.time > self.val:
			self.time = time()
			print("JOYSTICK POSITION:\nFront/back: {:>6.3f}\nLeft/right: {:>6.3f}\nYaw: {:>6.3f}\nThrottle: {:>6.3f}".format(
		self.joystick.get_axis(1), self.joystick.get_axis(0), self.joystick.get_axis(3), self.joystick.get_axis(2)))
			for i in range(self.numhats):
				print("HAT {} POSITION: {}".format(i, str(self.joystick.get_hat(i))))

		for i in range(self.numbuttons):
			if self.buttons[i] == 0 and self.joystick.get_button(i) == 1:
				self.buttons[i] = 1
				print("Button {} pressed.".format(i))
			elif self.buttons[i] == 1 and self.joystick.get_button(i) == 0:
				self.buttons[i] = 0
				print("Button {} released.".format(i))

		# If you remove this line the code breaks. Don't ask me why
		for event in pygame.event.get():

		# We have finished the item out of the queue. Allow it to enter again
		# * This needs to remain the last line *
		self.inQueue = False

	# Prints out the joystick data
	def print_joy_data(self, joyData):
		pass
