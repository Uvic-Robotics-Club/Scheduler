import threading
import queue
from time import sleep, time
from scheduler_types import *

class Scheduler:
	# Defined constants for the operation of the `poll_loop()` target thread
	POLL_THREAD_START_TIMEOUT_SEC = 5.00
	POLL_THREAD_MINIMUM_POLL_TIME_SEC = 0.01

	# Defined constants for the operation of the `event_loop()` target thread
	EVENT_THREAD_START_TIMEOUT_SEC = 5.00
	EVENT_THREAD_BLOCKED_POLL_INTERVAL_SEC = 0.01

	# Defined constants for the operation of the `funct_runner()` target thread
	FUNCT_RUNNER_THREAD_START_TIMEOUT_SEC = 0.50

    # Define the minimum thread count required by the Scheduler to fulfill its purpose. The minimum thread 
	# count is 1, since at least 1 worker thread is required for a task at any time.
	MIN_WORKER_THREAD_COUNT = 1

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

		if type(maxThreadCount) != int:
			return

		for function in pollFunctionsList:
			if callable(function) == False: 
				return

		self.activeThreads = []
		self.threadCount = 0
		self.threadCountLock = threading.Lock()
		self.pollFunctionsList = pollFunctionsList
		self.taskQueue = queue.PriorityQueue()
		
		if maxThreadCount >= self.MIN_WORKER_THREAD_COUNT:
			self.maxThreadCount = maxThreadCount
		else:
			self.maxThreadCount = self.MIN_WORKER_THREAD_COUNT

		self.active = False

	def run(self):
		""" Starts the instance of the Scheduler class, by starting the two necessary threads targetting
		`poll_loop()` and `event_loop()` respectively. If any of the two threads fail to start, then exit
		the scheduler.

		Args:
		  None
		Returns:
		- (bool) - Returns only `False` if any of the two threads failed to start, otherwise `None`
		"""

		print("[INFO]: Starting the scheduler")

		self.active = True

        # Starts the thread with `poll_loop()` as the target
		startPollLoopEvent = threading.Event()
		self.pollLoopThread = threading.Thread(target=self.poll_loop, args=(startPollLoopEvent,))
		self.pollLoopThread.start()

		if startPollLoopEvent.wait(timeout=self.POLL_THREAD_START_TIMEOUT_SEC) != True:
			print("[ERROR]: Failed to start Poll loop thread - Exiting scheduler.")
			self.active = False
			return False
		else:
			print("[INFO]: Poll loop thread started.")

		# Starts the thread with `event_loop` as the target. Increments the thread count if successful
		startEventLoopEvent = threading.Event()
		self.eventLoopThread = threading.Thread(target=self.event_loop, args=(startEventLoopEvent,))
		self.eventLoopThread.start()
		print("[INFO]: Event loop thread started.")

		# Starts the watchdog loop to monitor and kill threads
		self.watchdogLoopThread = threading.Thread(target=self.watchdog_loop)
		self.watchdogLoopThread.start()

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
		print("[INFO]: Poll loop thread terminated.")

		self.eventLoopThread.join()
		print("[INFO]: Event loop thread terminated.")

		# Check for any tasks in the priority queue that have not been processed by the event loop
		if not self.taskQueue.empty():
			print("[WARNING]: Priority queue is not empty. Emptying Priority queue.")
			self.taskQueue = queue.PriorityQueue()

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

		# Close this thread if there aren't any poll functions stored in the list
		if len(self.pollFunctionsList) == 0:
			print("[ERROR]: No poll functions - closing thread.")
			return

		startPollLoopEvent.set()

		timer = threading.Event()
		currTime = time() 
		while self.active:
			prevTime = currTime
			if currTime - prevTime < self.POLL_THREAD_MINIMUM_POLL_TIME_SEC:
				timer.wait(self.POLL_THREAD_MINIMUM_POLL_TIME_SEC - (currTime - prevTime))
			for function in self.pollFunctionsList:
				result = function()
				self.pushQueueTasks(result)


	# TODO: add some way to kill a thread that takes too long
	# Handles tasks from priority queue
	def event_loop(self, startEventLoopEvent):
		""" The target of the event function thread. Blocks until the Scheduler is active, and continuously 
		attempts to get the next task off `taskQueue`. A thread is then started for each task, with
		`funct_runner()` as the target.

		Args:
		- startEventLoopEvent (threading.Event): An Event instance on which `.set()` is called at the beginning
		    of the method to indicate successful thread startup
		Returns:
		  None
		"""

		timer = threading.Event()
		while self.active:
			if self.threadCount < self.maxThreadCount and self.taskQueue.qsize() > 0:
				# Since queue.PriorityQueue.qsize() does not guarantee that a subsequent call to get()
				# will not block, necessary to handle the failure case.
				try:
					obj = self.taskQueue.get(block=False)
				except queue.Empty:
					print("[WARNING]: Attempted to get task from empty Priority Queue")
					continue

				startFunctionRunnerEvent = threading.Event()
				
				
				
				t = threading.Thread(target=self.funct_runner, args=[obj.func, obj.args, startFunctionRunnerEvent])
				t.start()
				self.activeThreads.append([t, time()])
				self.incrementThreadCount()

			else:
				timer.wait(self.EVENT_THREAD_BLOCKED_POLL_INTERVAL_SEC)

	def watchdog_loop(self):
		pass

	# Takes a single task from the queue, runs it, and places the returned task(s) back in the queue
	# inputs: target: a function, taking 0 or one arguments
	# args: a single argument (can be anything) or None. Not passed to function if given None
	def funct_runner(self, target, args, startFunctionRunnerEvent):
		""" The target of each task thread, a wrapper for executing priority 
		queue tasks. If the task, a callable object, returns a result, then 
		place each element of the result onto a priority queue

		Args:
		- target (callable): A function to be run, i.e the task that has been popped from the
		    priority queue
		- args (list): The arguments that are passed to `target` when executed
		- startFunctionRunnerEvent (threading.Event): An Event instance on which `.set()` is called at the beginning
		    of the method to indicate successful thread startup
		Returns:
		  None

		"""

		if args:
			result = target(args)
		else:
			result = target()

		self.pushQueueTasks(result)

		# TODO: Move to end of function, where indicating success
		startFunctionRunnerEvent.set()

	def pushQueueTasks(self, taskList):
		
		if taskList == None:
			return True
		elif type(taskList) == list:
			for task in taskList:
				if type(task) == Pq_obj:
					self.taskQueue.put(task)
				else:
					print("[ERROR]: Failed to add object, wrong type!")
					return False
		elif type(taskList) == Pq_obj:
			self.taskQueue.put(taskList)
		else:
			print("[ERROR]: Failed to add task, wrong type!")
			return False

		return True
				
	def incrementThreadCount(self):
		""" A thread-safe wrapper to the local `threadCount` variable, allowing it 
		to be incremented in an atomic operation using the locally defined lock.

		Args:
		  None
		Returns:
		  (bool) - Returns only True when the local `threadCount` variable has been incremented
		"""

		with self.threadCountLock:
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

		with self.threadCountLock:
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
	scheduler.run()			# Start both loops
	sleep(6)
	scheduler.stop()


if __name__ == "__main__":
	main()
