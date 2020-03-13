import queue
from scheduler_types import Task
from taskpriority import TaskPriority
from time import time
import threading

class WorkerThreadManager():
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

    def __init__(self):
        self.active = True
        self.activeTaskThreads = dict([(priority, []) for priority in self.TASK_THREADS_SETTINGS.keys()])
        self.taskQueues = dict([(priority, queue.Queue()) for priority in self.TASK_THREADS_SETTINGS.keys()])

    def pushTask(self, task):
        if type(task) != Task:
            return 
        self.taskQueues[task.priority].put(task)

    def routing_loop(self):
        while self.active == True:
            for taskQueuePriority in self.taskQueues:
                if self.taskQueues[taskQueuePriority].empty():
                    continue

                for taskThreadPriority in [priority for priority in self.activeTaskThreads.keys() if priority <= taskQueuePriority].sort(reverse=True):
                    # Checks if space available for given priority. If available,
                    # start a thread and append to the given priority's list of threads 
                    if len(self.activeTaskThreads[taskThreadPriority]) < self.TASK_THREADS_SETTINGS[taskThreadPriority]['maxThreads']:
                        pendingTask = self.taskQueues[taskQueuePriority].get()

                        worker = Worker(self.taskQueues)
                        t = threading.Thread(target=self.taskWorker, args=[pendingTask.func, pendingTask.args])
                        t.start()
                        self.activeTaskThreads[threadPriority].append(t)
                        break

    def watchdog_loop(self):
        while self.active == True:
            for priority in self.activeTaskThreads:
                for thread in self.activeTaskThreads[priority]:
                    if (time() - self.activeTaskThreads[priority][thread].startTime) > self.TASK_THREADS_SETTINGS[priority]['taskTimeoutSec']:
                        # Somehow kill the thread


        
class Worker:
    def __init__(self, taskQueues, task):
        self.taskQueues = taskQueues
        self.task = task
        self.startTime = time()

    def run(self):
        if self.task.args:
            result = self.task.func(self.task.args)
        else:
            result = self.task.func() 

        self.pushTasksToQueues(result)

    def pushTasksToQueues(self, taskList):            
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

if __name__ == "__main__":
    m = WorkerThreadManager()
