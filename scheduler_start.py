import scheduler
import workAdder

from scheduler_types import *

# place all object imports here:
from joy_control import *
from joy_to_serial import *

def stupid_print():
	print("Here's your print statement, stupid")

def main():

	# Old version, pre-singleton...

	# # Initialize list of functions to poll
	# functs = []
	#
	# # Initialize and link all objects
	#
	# # Joystick input
	# joy = Joy_control()
	# # Make it so that the printer function is called as part of the event function
	# joy.add_function_to_call(joy.print_joy_data)
	# functs.append(joy.poll_function)
	#
	# # Link joystick to arduino (arm) control
	# ser = Arduino_arm_control()
	# joy.add_function_to_call(ser.write_to_arm)
	#
	# functs = []
	#
	# # Objects to demo multithreading. Don't actually do anything but print stuff
	# obj = scheduler.Demo_obj(2)
	# functs.append(obj.poll_function)
	# obj = scheduler.Demo_obj(1.2)
	# functs.append(obj.poll_function)
	#
	# # Initialize and start the program
	# # '8' is the maximum number of simultaneous threads, and 'functs' is the polling function list
	# s = scheduler.Scheduler(8, functs)
	# s.run()

	# Initialize list of functions to poll
	functs = []

	# Objects to demo multithreading. They just print stuff to show it's working
	# obj = scheduler.Demo_obj(2)
	# functs.append(obj.poll_function)
	# obj = scheduler.Demo_obj(1.2)
	# functs.append(obj.poll_function)

	# initialize joystick input
	joy = Joy_control()

	# Link joystick to arduino (arm) control
	ser = Arduino_arm_control()
	joy.add_function_to_call(ser.print_power)
	# joy.add_function_to_call(joy.print_joy_data)
	functs.append(joy.poll_function)



	# Initialize and start the program
	# '8' is the maximum number of simultaneous threads, and 'functs' is the polling function list
	s = scheduler.Scheduler(8, functs)
	# Create the workAdder singleton
	wA = workAdder.workAdder(s)
	s.run()
	obj = scheduler.Demo_obj(3.14)
	wA.add_pq_obj(Pq_obj(3, stupid_print))


if __name__ == '__main__':
	main()
