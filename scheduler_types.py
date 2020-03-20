from enum import Enum
from time import time

# Comparable object for storing a function and its arguments in the priority queue
# Sorts first by given priority number, then by timestamp
# Note: Low priority means it will run first!
class Pq_obj:
	def __init__(self, priority, func, args=None):
		self.func = func
		self.args = args
		self.priority = (priority, time())

	def __lt__(self, other):
		return self.priority < other.priority

class Task:
	def __init__(self, priority, func, args=None):
		self.func = func
		self.args = args
		self.priority = priority

	def __lt__(self, other):
		return self.priority < other.priority

class TaskPriority(Enum):
    HIGH = 1
    MEDIUM_HIGH = 2
    MEDIUM = 3
    MEDIUM_LOW = 4
    LOW = 5
    EXTENDED = 6

    #TODO: Document the method
    def __lt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value >= other.value

# A simple data type containing x, y, and z values
# Also has a handy print method!
class Vector3:

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "x = {}\ny = {}\nz = {}\n\n".format(self.x,self.y,self.z)
