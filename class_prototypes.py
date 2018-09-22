# This file contains code skeletons for a few common classes. These have no independent function,
# but may help when creating a new Python object.

# An object that can track
class Sample_obj:
	def __init__(self, pollRateSecs, functsOnEvent = None, maxInQueue=10):
		# The maximum poll rate of the object. Set to '0' for unlimited (note: this is still capped by main code)
		self.pollRate = pollRateSecs
		# Will store the last time the object has been polled. Used in logic to control rate
		self.time = time()
		# Limits how many of this object's event functions can be in the queue at the same time.
		# Most commonly will be 1 for objects that get data in the event function (most recent data),
		# or about 10 for functions that record data when polled (need every instance to be processed in order)
		self.maxInQueue = maxInQueue
		# Stores current number in queue
		self.inQueueCount = 0
		self.functs = functsOnEvent

	# Add this function to shell's poll list. For consistency, do not rename.
	def poll_function(self):

		if time() - self.time > self.pollRate and self.inQueueCount < self.maxInQueue:
			# Update internal time to when it was most recently added to the queue
			self.time = time()

			# -------------   Optional: ADD CODE HERE   -------------

			self.inQueueCount += 1
			# 3 is the average priority. Lower priorities go first.
			return Pq_obj(3, self.event_function)

	# Prints out thread
	def event_function(self):
		if self.functs:
			for f in self.functs:
				f()

		# Indicate when finished
		self.inQueueCount -= 1
