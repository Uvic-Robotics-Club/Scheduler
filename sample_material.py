from scheduler_types import Pq_obj

from time import time, sleep


# Simple object for testing Scheduler. Uses a polled timer to add a task to the queue, which then prints
class Self_contained_timer:
	def __init__(self, val):
		self.val = val
		self.time = time()

	# Ensures this doesn't happen more often than every val seconds
	def poll_function(self):
		if time() - self.time > self.val:
			self.time = time()
			#3 is the priority of this event
			return [Pq_obj(3, self.event_function)]

	# Checks that functions can be returned by polled functions
	def event_function(self):
		print("Event function " + str(self.val) + " is running on a thread")
		return [Pq_obj(3, self.do_later_function, self.val + 1)]

	# checks that functions can be returned by functions in queue
	def do_later_function(self, num):
		print("This ran a bit later from event function " + str(num - 1))


class Simple_producer:
	def __init__(self):
		self.time = time()
		self.number = 0
		self.functs = []

	# Run every 1 second
	def poll_function(self):
		if time() - self.time > 1:
			# Note that this implementation actually runs once per second, rather than the
			# approximate implementation in Self_contained_timer
			self.time += 1
			# 2 is the priority of this event - a higher priority than the average of '3'
			return [Pq_obj(3, self.event_function)]

	# When poll function determines something should happen, this is where it actually happens
	# It's okay to take a bit of time here, but do not block.
	def event_function(self):
		# Do any internal work
		self.number += 1

		# Get ready all the functions that are supposed to run on an event.
		# We won't actually run them here - we'll give them back to the scheduler to run when
		# it is ready to
		todo = []
		if self.functs:
			for f in self.functs:
				todo.append(Pq_obj(3, f, self.number))

		return todo

	# Provides a way to link functions from other objects to events from this producer.
	# Note: it is the consumer's responsibility to
	def add_function_to_call(self, function):
		self.functs.append(function)


class Simple_middleman:
	def __init__(self):
		# list of functions this class will call
		self.functs = []

	# When poll function determines something should happen, this is where it actually happens
	# It's okay to take a bit of time here, but do not block.
	def on_event(self, number):

		# Do any internal work
		# Note: this sleep is for demonstrational purposes only.
		# DO NOT use sleep calls in your own code, as they will block the scheduler
		sleep(5)

		# Get ready all the functions that are supposed to run on an event.
		# We won't actually run them here - we'll give them back to the scheduler to run when
		# it is ready to
		todo = []
		if self.functs:
			for f in self.functs:
				todo.append(Pq_obj(3, f, self.number))

		return todo


	# Provides a way to link functions from other objects to events from this producer.
	# Note: it is the consumer's responsibility to
	def add_function_to_call(self, function):
		self.functs.append(function)


class Simple_consumer:
	def __init__(self, modNum):
		self.modNum = modNum
		self.total = 0

	def on_event(self, number):
		self.total += number
		if self.total % self.modNum is 0:
			print(self.total, 'is divisible by', self.modNum)
