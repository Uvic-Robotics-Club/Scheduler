import serial.tools.list_ports
import serial


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
		print("check")
		for port in self.COM_ports:
			# print(port)
			if arduino_id in port:
				return self.COM_ports[port]
		return None


	def read_from_serial(self, ser, BAUD_RATE):
		print("check")
		# the messages sent and received are contained in brackets
		PACKET_START_MARKER = '>'
		PACKET_END_MARKER = '<'

		# signal read is stored in the variabe read_input
		read_input = ''
		reading_in_progress = True

		while reading_in_progress:

			# read from serial
			tmp_char = ser.read().decode('utf-8')
			if(tmp_char == PACKET_START_MARKER):
				while True:
					tmp_char = ser.read().decode('utf-8')

					# is closing marker is read, the message is over; otherwise keep reading
					if tmp_char != PACKET_END_MARKER:
						read_input += tmp_char
					else:
						reading_in_progress = False
						break;

		# printing to screen for debugging purposes. can be removed when the system has been tested to work well
		# print(read_input)

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

		for port in ports:
			print("check")

			if ('usb') in port[0] or ('COM') in port[0]:
				# opens the serial connection with the port, specifying baudrate & using read and write  
				# timeout of less than 1/10th of a second.
				# Arduino_Serial = serial.Serial(port.device, BAUD_RATE, timeout=0.05, write_timeout=0.05)
				Arduino_Serial = serial.Serial(port.device, BAUD_RATE, timeout = 1)


				# arduino_id_response = ''
				# # if the read times-out, we try again until we get its response.
				# while(not arduino_id_response):
				# 	Arduino_Serial.write(b'id')
				# 	arduino_id_response = str(Arduino_Serial.read(5), encoding='ascii')
				# a simple message to the arduino signalling a response has been received
				Arduino_Serial.write('id'.encode())

				# while loop to make sure the arduino has received the message by received a "done!" string
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
					print("unsuccessful connection with" + port_COM)

				self.COM_ports[arduino_id_response] = Arduino_Serial




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



