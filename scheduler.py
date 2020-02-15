import threading
import queue
from time import sleep, time
from scheduler_types import *

class Scheduler:
	# Defined constants for the operation of the `poll_loop()` target thread
	POLL_THREAD_START_TIMEOUT_SEC = 5.00
	POLL_THREAD_ACTIVE_POLL_INTERVAL_SEC = 0.01
	POLL_THREAD_MINIMUM_POLL_TIME_SEC = 0.01

	# Defined constants for the operation of the `event_loop()` target thread
	EVENT_THREAD_START_TIMEOUT_SEC = 5.00
	EVENT_THREAD_ACTIVE_POLL_INTERVAL_SEC = 0.01
	EVENT_THREAD_BLOCKED_POLL_INTERVAL_SEC = 0.01

	# Defined constants for the operation of the `funct_runner()` target thread
	FUNCT_RUNNER_THREAD_START_TIMEOUT_SEC = 0.50

    # Define the minimum thread count required by the Scheduler to fulfill its purpose. The minimum thread 
	# count is 3, where each thread is allocated as follows:
	#     - Threads 1 & 2: Assigned for the poll loop and event loop
	#     - Thread 3: Assigned to handle `funct_runner` targets.
	MINIMUM_THREAD_COUNT = 3

	def __init__(self, maxThreadCount, pollFunctionsList):
		""" Construct an instance of the Scheduler class.
		Once the instance is constructed, the state of the Scheduler is set to not active.

		Args:
		- threadCount (int): The maximum number of active threads permitted on the Scheduler instance
		- pollFunctionsList (list): A list of "callable" elements, as defined by `callable(listElement)` returning True.
	          These elements will be polled at an interval defined by `THREAD_POLL_MINIMUM_POLL_TIME_SEC`
		Returns:
		  None
		"""

		self.threadCount = 0
		self.pollFunctionsList = pollFunctionsList
		self.priorityQueue = queue.PriorityQueue()
		self.lock = threading.Lock()

		if maxThreadCount >= self.MINIMUM_THREAD_COUNT:
			self.maxThreadCount = maxThreadCount
		else:
			self.maxThreadCount = self.MINIMUM_THREAD_COUNT

		self.active = False

	def start(self):
		""" Starts the instance of the Scheduler class, by starting the two necessary threads targetting
		`poll_loop()` and `event_loop()` respectively. If any of the two threads fail to start, then exit
		the scheduler. If the method completes successfully, sets the state of the scheduler to Active.

		Args:
		  None
		Returns:
		- (bool) - Returns only `False` if any of the two threads failed to start, otherwise `None`
		"""

		print("Starting the scheduler")

        # Starts the thread with `poll_loop()` as the target. Increments the thread count if successful
		startPollLoopEvent = threading.Event()
		self.pollLoopThread = threading.Thread(target=self.poll_loop, args=(startPollLoopEvent,))
		self.pollLoopThread.start()
		if startPollLoopEvent.wait(timeout=self.POLL_THREAD_START_TIMEOUT_SEC) != True:
			print("[ERROR]: Failed to start Poll loop thread - Exiting scheduler.")
			# TODO: Raise Exception? May be used to handle failure case
			return False
		else:
			print("[INFO]: Poll loop thread started.")
			self.incrementThreadCount()

		# Starts the thread with `event_loop` as the target. Increments the thread count if successful
		startEventLoopEvent = threading.Event()
		self.eventLoopThread = threading.Thread(target=self.event_loop, args=(startEventLoopEvent,))
		self.eventLoopThread.start()
		if startEventLoopEvent.wait(timeout=self.EVENT_THREAD_START_TIMEOUT_SEC) != True:
			print("[ERROR]: Failed to start Event loop thread - Exiting scheduler.")
			# TODO: Raise Exception? May be used to handle failure case
			return False
		else:
			print("[INFO]: Event loop thread started.")
			self.incrementThreadCount()

		self.active = True

	def stop(self):
		""" Stops the instance of the Scheduler class in such a way that it can be restarted with a subsequent
		call to `start()`. Attempts to terminate the `poll_loop()` and `event_loop()` target threads, and
		empties the priority queue of any left over tasks.

		Args:
	      None
		Returns:
		- (bool) - Returns only `True` when both threads have terminated successfully, and 
		      the priority queue is emptied
		"""

		self.active = False
		print("[INFO]: Stopping the scheduler...")

		self.pollLoopThread.join()
		self.decrementThreadCount()
		print("[INFO]: Poll loop thread terminated.")

		self.eventLoopThread.join()
		self.decrementThreadCount()
		print("[INFO]: Event loop thread terminated.")

		# Check for any tasks in the priority queue that have not been processed by the event loop
		if not self.priorityQueue.empty():
			print("[WARNING]: Priority queue is not empty. Emptying Priority queue.")
			self.priorityQueue = queue.PriorityQueue()

		return True

	# Loops through every polling function
	def poll_loop(self, startPollLoopEvent):
		""" The target of the polling function thread. Blocks until the Scheduler is active, and polls 
		each `callable` element of `pollFunctionsList`, and puts each callable's result onto the priority
		queue. Each pushed result is of type `Pq_obj`, and is referred to as a "task".

		Args:
		- startPollLoopEvent (threading.Event): An Event instance on which `.set()` is called at the beginning
		      of the method to indicate successful thread startup
		Returns:
		  None 
		"""

		startPollLoopEvent.set()

		# Blocks until the scheduler is set to active
		while not self.active:
			sleep(self.POLL_THREAD_ACTIVE_POLL_INTERVAL_SEC)

		# Close this thread if there aren't any poll functions stored in the list
		if len(self.pollFunctionsList) == 0:
			print("[ERROR]: No poll functions - closing thread.")
			return

		# Loop through all polling functions
		timer = threading.Event()
		while self.active and not timer.wait(self.POLL_THREAD_MINIMUM_POLL_TIME_SEC):
			for function in self.pollFunctionsList:
				result = function()
				if result:
					for pq_obj in result:
						self.priorityQueue.put(pq_obj)

	# TODO: add some way to kill a thread that takes too long
	# Handles tasks from priority queue
	def event_loop(self, startEventLoopEvent):
		""" The target of the event function thread. Blocks until the Scheduler is active, and continuously 
		attempts to get the next task off `priorityQueue`. A thread is then started for each task, with
		`funct_runner()` as the target.

		Args:
		- startEventLoopEvent (threading.Event): An Event instance on which `.set()` is called at the beginning
		    of the method to indicate successful thread startup
		Returns:
		  None
		"""

		startEventLoopEvent.set()

		# Blocks until the scheduler is set to active
		while not self.active:
			sleep(self.EVENT_THREAD_ACTIVE_POLL_INTERVAL_SEC)

		while self.active:
			if self.threadCount < self.maxThreadCount and self.priorityQueue.qsize() > 0:
				# Since queue.PriorityQueue.gsize() does not guarantee that a subsequent call to get()
				# will not block, necessary to handle the failure case.
				try:
					obj = self.priorityQueue.get(block=False)
				except queue.Empty:
					print("[WARNING]: Attempted to get task from empty Priority Queue")
					continue

				startFunctionRunnerEvent = threading.Event()
				t = threading.Thread(target=self.funct_runner, args=[obj.func, obj.args, startFunctionRunnerEvent])
				t.start()
				if startFunctionRunnerEvent.wait(timeout=self.FUNCT_RUNNER_THREAD_START_TIMEOUT_SEC) != True:
					print("[ERROR]: Failed to start Function Runner thread for a task. Ignoring task.")
				else:
					pass
				    # TODO: Keep track of active threads. This will allow us to detect threads that are blocking and taking too long.
					#self.incrementThreadCount()

			else:
				sleep(self.EVENT_THREAD_BLOCKED_POLL_INTERVAL_SEC)

	# Takes a single task from the queue, runs it, and places the returned task(s) back in the queue
	# inputs: target: a function, taking 0 or one arguments
	# args: a single argument (can be anything) or None. Not passed to function if given None
	def funct_runner(self, target, args, startFunctionRunnerEvent):
		"""
		TODO: Complete method docstring
		"""

		startFunctionRunnerEvent.set()

		res = None
		if args:
			res = target(args)
		else:
			res = target()
		if res:
			for funct in res:
				self.priorityQueue.put(funct)
				
	def incrementThreadCount(self):
		""" A thread-safe wrapper to the local `threadCount` variable, allowing it 
		to be incremented in an atomic operation using the locally defined lock.

		Args:
		  None
		Returns:
		  (bool) - Returns only True when the local `threadCount` variable has been incremented
		"""

		with self.lock:
			self.threadCount += 1
		return True

	def decrementThreadCount(self):
		""" A thread-safe wrapper to the local `threadCount` variable, allowing it 
		to be decremented in an atomic operation using the locally defined lock.

		Args:
		  None
		Returns:
		  (bool) - Returns only True when the local `threadCount` variable has been decremented
		"""

		with self.lock:
			self.threadCount -= 1
		return True


# -------------------------------------------------------------------------------------------
# Below this line is NOT part of Scheduler's implementation


# Simple object for testing Scheduler. Uses a polled timer to add a task to the queue, which then prints
class Demo_obj:
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
		# Note: testing purposes only. NEVER put a sleep call in a real module!
		# sleep(10)
		return [Pq_obj(3, self.do_later_function, self.val + 1)]

	# checks that functions can be returned by functions in queue
	def do_later_function(self, num):
		print("This ran a bit later from event function " + str(num - 1))


# A demo for how to use.
# Note: should actually be set up and called through a separate 'start.py' file
def main():
	functions = []
	obj = Demo_obj(1.11)
	functions.append(obj.poll_function)
	obj = Demo_obj(1.414)
	functions.append(obj.poll_function)

	scheduler = Scheduler(8, functions)
	scheduler.start()			# Start both loops
	sleep(6)
	scheduler.stop()


if __name__ == "__main__":
	main()
