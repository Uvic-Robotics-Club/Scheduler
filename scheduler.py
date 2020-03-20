import queue
from scheduler_types import Task
from taskpriority import TaskPriority
from time import time, sleep
import threading

class Scheduler():
    POLL_THREAD_MINIMUM_POLL_TIME_SEC = 0.01

    TASK_THREADS_SETTINGS = {
        TaskPriority.HIGH: {
            'maxThreads': 5, 
            'taskTimeoutSec': 10
        },
        TaskPriority.MEDIUM: {
            'maxThreads': 3,
            'taskTimeoutSec': 5
        },
        TaskPriority.LOW: {
            'maxThreads': 1,
            'taskTimeoutSec': 2
        }
    }

    def __init__(self, pollFunctionsList):
        for function in pollFunctionsList:
            if callable(function) == False:
                return # TODO: Throw exception

        self.pollFunctionsList = pollFunctionsList
        self.taskQueues = dict([(priority, queue.Queue()) for priority in self.TASK_THREADS_SETTINGS.keys()])

        self.activeTaskThreads = dict([(priority, {}) for priority in self.TASK_THREADS_SETTINGS.keys()])
        self.activeTaskThreadLocks = dict([(priority, threading.Lock()) for priority in self.TASK_THREADS_SETTINGS.keys()])

    def start(self):
        self.active = True 

        self.pollThread = threading.Thread(target=self.pollLoop)
        self.pollThread.start()

        self.eventThread = threading.Thread(target=self.eventLoop)
        self.eventThread.start()

        self.watchdogThread = threading.Thread(target=self.watchdogLoop)
        self.watchdogThread.start()

    def stop(self):
        self.active = False

        self.pollThread.join()
        self.eventThread.join()
        self.watchdogThread.join()

    def pollLoop(self):
        timer = threading.Event()
        currTime = time()
        while self.active == True:
            prevTime = currTime
            if currTime - prevTime < self.POLL_THREAD_MINIMUM_POLL_TIME_SEC:
                timer.wait(self.POLL_THREAD_MINIMUM_POLL_TIME_SEC - (currTime - prevTime))
            for function in self.pollFunctionsList:
                result = function()
                self.pushTask(result)

    def eventLoop(self):
        while self.active == True:
            for taskQueuePriority in self.taskQueues:
                if self.taskQueues[taskQueuePriority].empty():
                    continue

                availableTaskThreadPriorities = [priority for priority in self.activeTaskThreads.keys() if priority <= taskQueuePriority]
                availableTaskThreadPriorities.sort(reverse=True)
                for taskThreadPriority in availableTaskThreadPriorities:
                    # Checks if space available for given priority. If available,
                    # start a thread and append to the given priority's list of threads 
                    if len(self.activeTaskThreads[taskThreadPriority]) < self.TASK_THREADS_SETTINGS[taskThreadPriority]['maxThreads']:
                        task = self.taskQueues[taskQueuePriority].get()
                        t = threading.Thread(target=Worker, args=[task, self.pushTask])
                        t.start()

                        with self.activeTaskThreadLocks[taskThreadPriority]:
                            self.activeTaskThreads[taskThreadPriority][t] = time()
                        break

    def watchdogLoop(self):
        while self.active == True:
            for priority in self.activeTaskThreads:
                # https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
                # TODO: Add lock since we're manipulating the dictionary
                with self.activeTaskThreadLocks[priority]:
                    for thread in self.activeTaskThreads[priority]:
                        if self.isThreadStale(priority, thread):
                            del self.activeTaskThreads[priority][thread]

    def isThreadStale(self, priority, thread):
        if not thread.isAlive():
            return True
        elif (time() - self.activeTaskThreads[priority][thread]) > self.TASK_THREADS_SETTINGS[priority]['taskTimeoutSec']:
            # Kill thread here
            return True
        else:
            return False

    def pushTask(self, taskList):            
        if taskList == None:
            return True
        elif type(taskList) == list:
            for task in taskList:
                if type(task) == Task:
                    self.taskQueues[task.priority].put(task)
                else:
                    print("[ERROR]: Failed to add object, wrong type!")
                    return False
        elif type(taskList) == Task:
            self.taskQueues[task.priority].put(task)
        else:
            print("[ERROR]: Failed to add task, wrong type!")
            return False
        return True
                          
class Worker:
    def __init__(self, task, pushTaskFunc):
        self.task = task
        self.pushTask = pushTaskFunc

        self.run()

    def run(self):
        if self.task.args:
            result = self.task.func(self.task.args)
        else:
            result = self.task.func() 
        self.pushTask(result)

##########################################################################3


# Simple object for testing Scheduler. Uses a polled timer to add a task to the queue, which then prints
class Demo_obj:
	def __init__(self, val):
		self.val = val
		self.time = time()

	# Ensures this doesn't happen more often than every val seconds
	def poll_function(self):
		if time() - self.time > self.val:
			self.time = time()
			return [Task(TaskPriority.MEDIUM, self.event_function)]     

	# Checks that functions can be returned by polled functions
	def event_function(self):
		print("Event function " + str(self.val) + " is running on a thread")
		# Note: testing purposes only. NEVER put a sleep call in a real module!
		# sleep(10)
		return [Task(TaskPriority.HIGH, self.do_later_function, self.val + 1)]

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

	scheduler = Scheduler(functions)
	scheduler.start()			# Start both loops
	sleep(6)
	scheduler.stop()


if __name__ == "__main__":
	main()
