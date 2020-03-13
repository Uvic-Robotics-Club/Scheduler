import queue
from scheduler_types import *
from taskpriority import TaskPriority
import threading

class WorkerThreadManager():
    MAX_TASK_THREADS = {
        TaskPriority.HIGH: 5,
        TaskPriority.MEDIUM: 3,
        TaskPriority.LOW: 1
    }

    def __init__(self, priorityQueue):
        self.active = True

        self.activeTaskThreads = {
            TaskPriority.HIGH: [],
            TaskPriority.MEDIUM: [],
            TaskPriority.LOW: []
        }

        self.taskQueues = {
            TaskPriority.HIGH: queue.Queue(),
            TaskPriority.MEDIUM: queue.Queue(),
            TaskPriority.LOW: queue.Queue()
        }

        self.priorityQ



    def pushTask(self, task):
        if type(task) != Pq_obj:
            return 

        for priority in self.taskQueues.keys():
            if task.priority[0] == priority.value:
                self.taskQueues[priority].put(task)

    def routing_loop(self):
        while self.active == True:
            for priority in self.taskQueues:
                try:
                    pendingTask = self.taskQueues[priority].get(block=False)
                except queue.Empty:
                    continue

                # For a given priority, e.g TaskPriority.MEDIUM, must
                # check if any available space in both lists for 
                # TaskPriority.HIGH and TaskPriority.MEDIUM
                for threadPriority in self.activeTaskThreads:
                    if pendingTask.priority[0] > threadPriority.value and len(self.activeTaskThreads[threadPriority]) < self.MAX_TASK_THREADS[threadPriority]:
                        t = threading.Thread(target=self.taskWorker, args=[obj.func, obj.args, startFunctionRunnerEvent])
                        t.start()
                        self.activeTaskThreads[threadPriority].append(t)
                        break

    def watchdog_loop(self):
        pass

    def taskWorker(self, target, args):
		if args:
			result = target(args)
		else:
			result = target()

        self.pushQueueTa

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




if __name__ == "__main__":
    m = WorkerThreadManager()
