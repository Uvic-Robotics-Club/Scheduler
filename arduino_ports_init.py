import serial.tools.list_ports
import serial
import time


ports = list(serial.tools.list_ports.comports())

class Arduino_serial_finder:


	# The following is a constructor for this class, where a "Dictionary" is initialized. This
	# dictionary will hold all the serial port information of the arduinos connected to the
	# raspberry pi after they are registered when the ports are scanned.
	def __init__(self):
		self.COM_ports = {}



	# This is to identify the arduino based on its 'ID' and returns its serial information
	# if registered
	def get_serial_port(self, arduino_id):
		for port in self.COM_ports:

			if arduino_id in port:
				return self.COM_ports[port]
		return None



	def read_from_serial(self, Arduino_Serial, BAUD_RATE):
		print("Reading...")
		# the messages sent and received are contained in brackets
		PACKET_START_MARKER = '>'
		PACKET_END_MARKER = '<'

		# signal read is stored in the variabe read_input
		read_input = ''
		reading_in_progress = True
		
		while reading_in_progress:
			print("num of bytes = " + str(Arduino_Serial.in_waiting) + "  " +read_input)

			# read from serial
			tmp_char = Arduino_Serial.read().decode('utf-8')
			if(tmp_char == PACKET_START_MARKER):
				while Arduino_Serial.in_waiting:
					tmp_char = Arduino_Serial.read().decode('utf-8')

					# is closing marker is read, the message is over; otherwise keep reading
					if tmp_char != PACKET_END_MARKER:
						read_input += tmp_char
					else:
						reading_in_progress = False
						break;

		# while Arduino_Serial.in_waiting:
		# 	print(Arduino_Serial.read().decode('utf-8') + '---- ' + str(Arduino_Serial.in_waiting), end= '')


		# printing to screen for debugging purposes. can be removed when the system has been tested to work well
		print("Done reading. Input = " + read_input)
		return read_input


	# This function scans all the ports and registers a serial connection when an arduino is found
	# connected to it. It then uses the serial connection to interact with the arduino using read 
	# and write instructions.
	def scan_ports_initialize(self):

		NUMBER_OF_CONNECTED_ARDUINOS = 1
		ROVER_SERIAL_PORT = '' # TODO: Update to use the correct port # update 2!! no need to update cz the com port is detected automatically
		ARM_SERIAL_PORT = ''
		BAUD_RATE = 9600
		connected_arduinos_found = 0
		print("scanning now")

		for port in ports:
			print("port found: " + port.device)

			if ('USB') in port.device or ('COM') in port.device:
				# opens the serial connection with the port, specifying baudrate & using read and write  
				# timeout of less than 1/10th of a second.
				# Arduino_Serial = serial.Serial(port.device, BAUD_RATE, timeout=0.05, write_timeout=0.05)
				Arduino_Serial = serial.Serial(port.device, BAUD_RATE, timeout = 3)


				# delay has to be put because the arduino takes almost 1.7 seconds to be ready for receiving from Serial :(
				time.sleep(1.8)
				Arduino_Serial.write('>ID<'.encode())
	
				# wait till we receive a response
				while not Arduino_Serial.in_waiting:
					None

				# start reading what we received from Serial
				arduino_id_response = self.read_from_serial(Arduino_Serial, BAUD_RATE)


				# if read from serial did not timeout:
				if(len(arduino_id_response) > 0):
					# increment the number of arduinos connected
					secure_connection = True
					connected_arduinos_found += 1

					# figure which arduino is connected depending on the message sent by the arduino through serial
					if arduino_id_response == "Motor driver":
						print("Motor driver is connected!")


					if arduino_id_response == "Robot arm":
						print("Robot arm is connected!")

				else:
					print("unsuccessful connection with " + port.device)

				self.COM_ports[arduino_id_response] = Arduino_Serial



# main only for debugging
def main():
	asf = Arduino_serial_finder()
	asf.scan_ports_initialize()
	# get the serial based on the arduino's ID.
	connection = asf.get_serial_port("Motor driver")

	if(connection):
		print(connection)
	else:
		print('no connection')



if __name__ == '__main__':
	main()



