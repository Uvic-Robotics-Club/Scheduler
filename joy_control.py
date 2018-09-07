

class Joy_control:
	def __init__(self, val):
		self.inQueue = False

	def poll_function(self):
		# Prevents multiple of these objects in the queue
		if self.inQueue:
			return None

		# ADD CODE HERE

		self.inQueue = True
		return Pq_obj(3, self.event_function)

	# Prints out thread
	def event_function(self):

		# ADD CODE HERE

		# We have finished the item out of the queue. Allow it to enter again
		self.inQueue = False
