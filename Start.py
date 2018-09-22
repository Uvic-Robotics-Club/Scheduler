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
	joy.add_function_to_call(joy.print_joy_data)
	functs.append(joy.poll_function)

	# Link joystick to arduino (arm) control
	ser = Arduino_arm_control()
	joy.add_function_to_call(ser.write_to_arduino)

	# Start the program
	s = shell.Shell(8, functs)
	s.run()


if __name__ == '__main__':
	main()
