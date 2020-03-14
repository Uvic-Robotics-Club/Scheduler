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
        self.activeTaskThreads = dict([(priority, {}) for priority in self.TASK_THREADS_SETTINGS.keys()])
        self.taskQueues = dict([(priority, queue.Queue()) for priority in self.TASK_THREADS_SETTINGS.keys()])
        # TODO: add lock for each activeTaskThread element

    def start(self):
        self.active = True 

        self.routingThread = threading.Thread(target=self.routingLoop)
        self.routingThread.start()

        self.watchdogThread = threading.Thread(target=self.watchdogLoop)
        self.watchdogThread.start()

    def stop(self):
        self.active = False

        self.routingThread.join()
        self.watchdogThread.join()

    def pushTask(self, task):
        if type(task) != Task:
            return 
        self.taskQueues[task.priority].put(task)

    def routingLoop(self):
        while self.active == True:
            for taskQueuePriority in self.taskQueues:
                if self.taskQueues[taskQueuePriority].empty():
                    continue

                for taskThreadPriority in [priority for priority in self.activeTaskThreads.keys() if priority <= taskQueuePriority].sort(reverse=True):
                    # Checks if space available for given priority. If available,
                    # start a thread and append to the given priority's list of threads 
                    if len(self.activeTaskThreads[taskThreadPriority]) < self.TASK_THREADS_SETTINGS[taskThreadPriority]['maxThreads']:
                        task = self.taskQueues[taskQueuePriority].get()
                        t = threading.Thread(target=Worker, args=[self.taskQueues, task])
                        t.start()
                        self.activeTaskThreads[taskThreadPriority][t] = time()
                        break

    def watchdogLoop(self):
        while self.active == True:
            for priority in self.activeTaskThreads:
                # https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
                # TODO: Add lock since we're manipulating the dictionary
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
                          
class Worker:
    def __init__(self, taskQueues, task):
        self.taskQueues = taskQueues
        self.task = task

        self.run()

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
    m.start()
    m.stop()
