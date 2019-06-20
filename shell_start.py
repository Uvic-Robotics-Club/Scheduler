import shell

# place all object imports here:
from joy_control import *
from joy_to_serial import *

def main():
	# Initialize list of functions to poll
	functs = []

	# Initialize and link all objects

	# Joystick input
	joy = Joy_control()
	functs.append(joy.poll_function)

	joySplit = Joy_splitter()
	joy.add_function_to_call(joySplit.event_function)

	joySplit.add_function_to_call(joy.print_joy_data, 0)
	joySplit.add_function_to_call(joy.print_joy_data, 1)
	joySplit.add_function_to_call(joy.print_joy_data, 1)

	# Link joystick to lower arm control
	ser = Arduino_arm_control()
	joy.add_function_to_call(ser.write_to_arduino)

	# Initialize and start the program
	# '8' is the maximum number of simultaneous threads, and 'functs' is the polling function list
	s = shell.Shell(8, functs)
	s.run()


if __name__ == '__main__':
	main()
