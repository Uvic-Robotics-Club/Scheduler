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


# A simple data type containing x, y, and z values
# Also has a handy print method!
class Vector3:

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "x = {}\ny = {}\nz = {}\n\n".format(self.x,self.y,self.z)
