import shell

# place all object imports here:
from joy_control import *
from joy_to_serial import *

def main():
	# Initialize list of functions to poll
	functs = []

	# Initialize and link all objects

	# Start the program
	s = shell.Shell(8, functs)


if __name__ == '__main__':
	main()
