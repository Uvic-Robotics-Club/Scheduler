import queue
from scheduler_types import Task
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

        self.priorityQueue = priorityQueue

    def pushTask(self, task):
        if type(task) != Task:
            return 

        self.taskQueues[task.priority].put(task)

    def routing_loop(self):
        while self.active == True:
            for taskQueuePriority in self.taskQueues:
                if self.taskQueues[taskQueuePriority].empty():
                    continue

                for taskThreadPriority in [priority for priority in self.activeTaskThreads.keys()]:

                #for threadPriority in self.activeTaskThreads:
                #    if pendingTask.priority[0] > threadPriority.value and len(self.activeTaskThreads[threadPriority]) < self.MAX_TASK_THREADS[threadPriority]:
                #        t = threading.Thread(target=self.taskWorker, args=[pendingTask.func, pendingTask.args])
                #        t.start()
                #        self.activeTaskThreads[threadPriority].append(t)
                #        break

                pendingTask = self.taskQueues[priority].get(block=False)

    def watchdog_loop(self):
        pass

    def taskWorker(self, target, args):
        if args:
            result = target(args)
        else:
            result = target()

        self.pushQueueTasks(result)
        
    def pushQueueTasks(self, taskList):
        if taskList == None:
            return True
        elif type(taskList) == list:
            for task in taskList:
                if type(task) == Task:
                    self.priorityQueue.put(task)
                else:
                    print("[ERROR]: Failed to add object, wrong type!")
                    return False
        elif type(taskList) == Task:
            self.priorityQueue.put(taskList)
        else:
            print("[ERROR]: Failed to add task, wrong type!")
            return False
        return True           

if __name__ == "__main__":
    m = WorkerThreadManager(queue.PriorityQueue())
