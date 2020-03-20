from scheduler import Scheduler
from scheduler_types import Task, TaskPriority
import queue
import threading
import time
import unittest 

class SchedulerTests(unittest.TestCase):

    def testConstructorWithValidPollFunctions(self):
        pollFunctionsList = [self.exampleFunctionSleep] * 5
        expectedPriorities = [TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]

        scheduler = Scheduler(pollFunctionsList)

        # Check that poll functions are preserved
        self.assertListEqual(pollFunctionsList, scheduler.pollFunctionsList)

        # Check that the expected priorities are present in task queues
        self.assertListEqual(expectedPriorities, list(scheduler.taskQueues.keys()))
        # Check that empty queues present in task queues
        self.assertEqual(len(expectedPriorities), len(scheduler.taskQueues.values()))
        for taskQueue in scheduler.taskQueues:
            self.assertEqual(queue.Queue, type(scheduler.taskQueues[taskQueue]))
            self.assertTrue(scheduler.taskQueues[taskQueue].empty())

        # Check that active task threads list elements are present
        self.assertListEqual(expectedPriorities, list(scheduler.activeTaskThreads.keys()))
        # Check that empty dictionaries present in active task thread list
        self.assertListEqual([{}] * len(expectedPriorities), list(scheduler.activeTaskThreads.values()))

        # Check that the expected priorities are present in task thread list locks
        self.assertListEqual(expectedPriorities, list(scheduler.activeTaskThreadLocks.keys()))
        # Check that unlocked locks are present in list
        self.assertEqual(len(expectedPriorities), len(scheduler.taskQueues.values()))
        for threadListLock in scheduler.activeTaskThreadLocks:
            self.assertFalse(scheduler.activeTaskThreadLocks[threadListLock].locked())

    def testConstructorWithInvalidPollFunctions(self):
        # Test with invalid data type
        pollFunctionsList = [self.exampleFunctionSleep, "None"]
        with self.assertRaises(Exception):
            Scheduler(pollFunctionsList)

        # Test with empty list
        pollFunctionsList = []
        with self.assertRaises(Exception):
            Scheduler(pollFunctionsList)

        # Test with a dictionary, i.e not a list
        pollFunctionsList = {"func1": self.exampleFunctionSleep}
        with self.assertRaises(Exception):
            Scheduler(pollFunctionsList)

    def exampleFunctionSleep(self):
        time.sleep(10)


if __name__ == '__main__':
    unittest.main()