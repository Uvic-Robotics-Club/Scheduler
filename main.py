import serial.tools.list_ports
import serial
import time

ports = list(serial.tools.list_ports.comports())

class Arduino_serial_finder:

	def __init__(self):
		self.book = {}


	def get_serial(self, arduino_id):
		if arduino_id in self.book:
			return self.book[arduino_id]
		else:
			return None



	def scan_ports_initialize(self):
		ArduinoUnoSerials = []
		for i in ports:
			for j in i:
				if ('Arduino') in j or ('USB') in j:
					print(i)
					print("Found Arduino")

					ArduinoUnoSerial = serial.Serial(i[0], 9600, timeout = 3)
					ArduinoUnoSerials.append(ArduinoUnoSerial)
		return ArduinoUnoSerials



	def scan_ports_comm(self, ArduinoUnoSerial):
		ArduinoUnoSerial.write(b'id')
		print("arduino's response to id request:")

		arduino_id_response = ''
		while(not arduino_id_response):
			arduino_id_response = str(ArduinoUnoSerial.readline()[:-2], encoding='ascii')
		print(arduino_id_response)

		self.book[arduino_id_response] = (ArduinoUnoSerial)
		ArduinoUnoSerial.close()


		print("there are arduinos at ports:")
		for i in self.book:
			print(i)


		print("done.")




def timeout_serial(timeout):
	endtime = time.time() + timeout
	while(True):
		remaining = endtime - time.time()
		if remaining <= 0:
			break




def main():
	asf = Arduino_serial_finder()
	ArduinoUnoSerials = asf.scan_ports_initialize()
	# timeout_serial(3)
	# asf.scan_ports_comm(ArduinoUnoSerials[0])
	connection = asf.get_serial('I am the little arduino')
	if connection:
		print(connection)
	else:
		print("no connection")



if __name__ == '__main__':
	main()


