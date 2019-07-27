# This class is imported anywhere that needs to be able to put work on the 'pq' priority queue in a Shell.
# Create an instance add_pq_obj to add work to the Shell's priority queue.
# The first instantiation of workAdder must be fed a Shell. After that, all subsequent instantiations do not need any parameters.

from shell_types import Pq_obj

class workAdder:

		# only one innerAdder can exist at once
		class innerAdder:
			def __init__(self, shell):
					self.shell = shell
			def __add_pq_obj__(self, new_PQObj):
				self.shell.pq.put(new_PQObj)

		instance = None # this is a class variable, meaning it is shared between all instances of the class

		def __init__(self, shell = None):
			if not shell == None:
				if not workAdder.instance:
					workAdder.instance = workAdder.innerAdder(shell)
		def get_property(self, name):
			return getattr(self.instance, name) # call __getattr__("shell") to get the innerAdder's shell
		def add_pq_obj(self, new_PQObj):
			if type(new_PQObj) == Pq_obj:
				self.instance.__add_pq_obj__(new_PQObj)
# 				TODO: non-Pq_obj inputs should trigger some kind of error routine
