import socket
import math
import traceback

VALUES_PER_SENSOR = 3


def extract_SensorData_v2(data_string):
	'''Extracts sensors'data from the input raw data string.
	The return object is an array of arrays [i][j], where i corresponds to sampled acquisitions and j corresponds to sensors' value.
	All sensors' values are represented as strings.

	This function replaces the __extractSensorData within HIMUServer.py because of a bug where it would 
	mix different sensor_values from different sensors and get rid of the trailing sensor_data

	Variable:
	packages - an unformatted list of strings containing all sensor's values
	packVal - a list of 3 strings (or 1 if its timestamp) containing sensor's xyz's values
	retVal - a list of packVals
	'''
	packages = data_string.split('\r\n')
	retVal = []
	for pack in packages:
		if pack != '':
			try:
				packVal = []
				packSplit = pack.replace('\n', '').replace('\r', '').split(",")
				numSensors = int(math.floor(len(packSplit) / VALUES_PER_SENSOR))
				# Checks if packSplit doesn't contain the sensor_name obtained from phone
				if packSplit[0].isdigit() and len(packSplit) != 1:
					p = [packSplit[0]]
					packVal.append(p)
					packSplit = packSplit[1:]
					for i in range(0, numSensors):
						p = packSplit[i * VALUES_PER_SENSOR : (i+1) * (VALUES_PER_SENSOR)]
						packVal.append(p)
					if len(packVal) > 0:
						retVal.append(packVal)
			except Exception as ex:
				pass
	return retVal