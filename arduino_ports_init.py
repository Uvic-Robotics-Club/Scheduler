import serial.tools.list_ports
import serial


ports = list(serial.tools.list_ports.comports())

class Arduino_serial_finder:


	# The following is a constructor for this class, where a "Dictionary" is initialized. This
	# dictionary will hold all the serial port information of the arduinos connected to the
	# raspberry pi after they are registered when the ports are scanned.
	def __init__(self):
		self.book = {}



	# This is to identify the arduino based on its 'ID' and returns its serial information
	# if registered
	def get_serial(self, arduino_id):
		for i in self.book:
			if arduino_id in i:
				return self.book[i]
		return None



	# This function scans all the ports and registers a serial connection when an arduino is found
	# connected to it. It then uses the serial connection to interact with the arduino using read 
	# and write instructions.
	def scan_ports_initialize(self):
		NumTrails = 1
		for i in ports:
			if ('usb') in i[0]:
				# opens the serial connection with the port, specifying baudrate & using read and write  
				# timeout of less than 1/10th of a second.
				ArduinoUnoSerial = serial.Serial(i[0], 9600, timeout=0.05, write_timeout=0.05)
				arduino_id_response = ''
				# if the read times-out, we try again until we get its response.
				while(not arduino_id_response):
					if NumTrails > 3:
						raise Exception('Error: Read instruction timed out multiple times; unable to read from arduino')
					ArduinoUnoSerial.write(b'id')
					arduino_id_response = str(ArduinoUnoSerial.read(5), encoding='ascii')
					NumTrails += 1
				self.book[arduino_id_response] = ArduinoUnoSerial




def main():
	asf = Arduino_serial_finder()
	asf.scan_ports_initialize()
	# get the serial based on the arduino's ID.
	connection = asf.get_serial('Nano')
	if(connection):
		print(connection)
	else:
		print('no connection')



if __name__ == '__main__':
	main()



