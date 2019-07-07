# This class is imported anywhere that needs to be able to put work on the 'pq' priority queue in a Shell.


class workAdder:

		# only one innerAdder can exist at once
		class innerAdder:
			def __init__(self, shell):
					self.shell = shell
			def add_pq_obj(self, new_PQObj):
				self.shell.pq.put(new_PQObj)

		instance = None # this is a class variable, meaning it is shared between all instances of the class

		def __init__(self, shell):
			if not workAdder.instance:
				workAdder.instance = workAdder.innerAdder(shell)
			else:
				workAdder.instance.shell = shell
		def __getattr__(selfself, name):
			return getattr(self.instance, name) # call __getattr__("shell") to get the innerAdder's shell
		def __add_pq_obj__(self, new_PQObj):
			self.instance.add_pq_obj(new_PQObj)