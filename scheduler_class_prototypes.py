# This file contains code skeletons for a few common classes. These have no independent function,
# but may help when creating a new Python object.


class Sample_producer:
	# Change parameters as needed. These two are recommended, but not required
	def __init__(self, maxPollRateSeconds, maxInQueue=10):
		# The maximum poll rate of the object. Set to '0' for unlimited (note: this is still capped by main code)
		self.pollRate = maxPollRateSeconds
		# Will store the last time the object has been polled. Used in logic to control rate
		self.time = time()
		# Limits how many of this object's event functions can be in the queue at the same time.
		# Most commonly will be 1 for objects that get data in the event function (most recent data),
		# or about 10 for functions that record data when polled (need every instance to be processed in order)
		self.maxInQueue = maxInQueue
		# Stores current number in queue
		self.inQueueCount = 0
		# Tracks all functions that should be called when an event happens
		self.functs = []
		# 3 is the average priority. Lower priorities go first.
		self.priority = 3

		# -------------   Optional: ADD CODE HERE   -------------
		# Note: most stuff should be linked in the start file instead of hard-coded.

	# Add this function to Scheduler's poll list. For consistency, do not rename.
	def poll_function(self):
		if time() - self.time > self.pollRate and self.inQueueCount < self.maxInQueue:
			# Update internal time to when it was most recently added to the queue
			self.time = time()

			# -------------   Optional: ADD CODE HERE   -------------
			# DO NOT add any code that takes a significant amount of time here.
			# DO NOT add anything that can block!

			self.inQueueCount += 1
			return [Pq_obj(self.priority, self.event_function)]

	# When poll function determines something should happen, this is where it actually happens
	# It's okay to take a bit of time here, but do not block.
	def event_function(self):
		# Run all the functions that are supposed to run on an event.
		doLater = []
		if self.functs:
			for f in self.functs:
				res = f()
				# Track anything we need to process later
				if res is not None:
					doLater.append(res)

		# -------------   Optional: ADD CODE HERE   -------------
		# Add any code that you want to happen on an event here.

		# Note: track when finished, not when started, so we can't spawn too many if the function
		# takes a lot of time
		self.inQueueCount -= 1
		if len(doLater > 0):
			return doLater

	# Provides a way to link functions from other objects to events from this producer.
	# Note: it is the consumer's responsibility to
	def add_function_to_call(self, function):
		self.functsToCall.append(function)
