import scheduler

# place all object imports here:
from joy_control import *
from joy_to_serial import *
from scheduler_class_prototypes import *

def main():
	# Initialize list of functions to poll
	functs = []

	# Initialize and link all objects

	# initialize joystick input
	joy = Joy_control()

	# Link joystick to console output
	joy.add_function_to_call(joy.print_joy_data)
	functs.append(joy.poll_function)

	# Link joystick to arduino (arm) control
	ser = Arduino_arm_control()
	joy.add_function_to_call(ser.write_to_arm)

	# Initialize and start the program
	# '8' is the maximum number of simultaneous threads, and 'functs' is the polling function list
	s = scheduler.Scheduler(8, functs)
	s.run()


if __name__ == '__main__':
	main()
