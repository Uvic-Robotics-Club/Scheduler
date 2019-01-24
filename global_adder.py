#The singleton needs to take a reference to the shell when it is instantiated
class GlobalAdder:
	class __GlobalAdder:
		def __init__(self, shell):
			self.shell = shell
	instance = None #there's our class variable. You get class variables by putting them here, outside the init function
	def __init__(self, shell):
		if not GlobalAdder.instance:
			GlobalAdder.instance = GlobalAdder.__GlobalAdder(shell) #does this line create a __GlobalAdder?
		else:
			GlobalAdder.instance.val = shell
	def __getattr__(self, name):
		return getattr(self.instance, name)
		#calling asdf.__getattr__("shell") will get the inner object's variable named shell
	