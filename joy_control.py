from shell import Pq_obj
from time import sleep

class Joy_control:
	def __init__(self):
		self.inQueue = False

	def poll_function(self):
		# Prevents multiple of these objects in the queue
		if self.inQueue:
			return None

		# ADD CODE HERE

		self.inQueue = True
		return Pq_obj(3, self.event_function, args=[])

	# Prints out thread
	def event_function(self):

		# ADD CODE HERE
		print("print")
		while True:
			continue


		# We have finished the item out of the queue. Allow it to enter again
		# This needs to remain the last line
		self.inQueue = False
