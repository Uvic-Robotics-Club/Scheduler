import threading
# TODO: Change to "queue" in python 3
import queue
from time import sleep, time

from joy_control import *


# Note: we can create objects and pass their methods into this object


class Shell:
	def __init__(self, threadCount, pollFunctionsList):
		self.pq = queue.PriorityQueue()
		self.stop = False
		self.minPollTime = 0.01

		self.pfl = pollFunctionsList
		# Requires at least 3 threads to run
		# Note that it is more efficient with more threads (less time burned in main threads)
		if threadCount < 3:
			threadCount = 3
		self.maxThreads = threadCount

	def run(self):
		self.stop = False
		t = threading.Thread(target=self.poll_loop)
		t.start()
		t = threading.Thread(target=self.event_loop)
		t.start()

	# Loops through every polling function
	def poll_loop(self):
		# Close this thread if there aren't any poll functions stored in the list
		if len(self.pfl) == 0:
			print("No poll functions - closing thread")
			return

		# Loop through all polling functions
		# TODO: add a minimum time before repetitions
		prevTime = time()
		currTime = time()
		while not self.stop:
			prevTime = currTime
			currTime = time()
			if currTime - prevTime < self.minPollTime:
				sleep(self.minPollTime - (currTime - prevTime))
			for f in self.pfl:
				res = f()
				if res:
					self.pq.put(res)

	# TODO: add some way to kill a thread that takes too long
	# Handles tasks from priority queue
	def event_loop(self):
		while not self.stop:
			if threading.active_count() < self.maxThreads and self.pq.qsize() > 0:
				obj = self.pq.get()
				t = threading.Thread(target=obj.func, args=obj.args)
				t.start()
			else:
				sleep(0.01)


# Comparable object for storing a function and its arguments in the priority queue
# Sorts first by given priority number, then by timestamp
class Pq_obj:
	def __init__(self, priority, func, args=[]):
		self.func = func
		self.args = args
		self.priority = (priority, time())

	def __lt__(self, other):
		return self.priority < other.priority


# Simple object for testing Shell. Uses a polled timer to add a task to the queue, which then prints
class Demo_obj:
	def __init__(self, val):
		self.val = val
		self.time = time()

	# Ensures this doesn't happen more often than every val seconds
	def poll_function(self):
		if time() - self.time > self.val:
			self.time = time()
			#3 is the priority of this event
			return Pq_obj(3, self.event_function)

	# Prints out thread
	def event_function(self):
		self.do_some_math()
		print("Event function " + str(self.val) + " is running on a thread")

	# Does nothing
	def do_some_math(self):
		x = self.val
		y = self.val
		x = x * y


class Temp:
	def __init__(self, updateFunctions):
		self.updateFunctions = updateFunctions
		self.temp

	def poll_function(self):
		return Pq_obj(3, self.event_function)

	def event_function(self):
		for function in self.updateFunctions:
			function(temp)


def main():
	functions = []
	obj = Demo_obj(1.11)
	functions.append(obj.poll_function)
	obj2 = Demo_obj(1.414)
	functions.append(obj2.poll_function)
	obj3 = Joy_control()
	functions.append(obj3.poll_function)

	obj4 = Temp(func1, func2, func3)
	functions.append(obj4.poll_function)

	shell = Shell(4, functions)
	shell.run() # Start both loops
	# sleep(6)
	# shell.stop = True


if __name__ == "__main__":
	main()
