#===============================================================================
#
# MIT License
#
# HyperIMU Server (HIMU Server)
# Copyright (c) [2017] [Sebastiano Campisi - ianovir]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#===============================================================================

import socket
import math
import traceback
import time
import json

valuesPerSensor = 3

class HIMUServer:

	def __init__(self, bufferSize = 2048, timeout = 10, separatorIndex = 0):
		self.__listeners = []
		self.__packSeparators = ["\r\n" , "#"]
		self.__commentSymbol = '@'
		self.timeout = timeout  #timeout in seconds
		self.bufferSize=bufferSize #bytes
		self.go = True		
		if(separatorIndex == 0):
			self.packSeparator = self.__packSeparators[0]
		else:
			self.packSeparator = self.__packSeparators[separatorIndex]
		
	def addListener(self , newListener):
		self.__listeners.append(newListener)

	def __notifyListeners(self, recPacket):
		for listener in self.__listeners:
			listener.notify(recPacket)

	def executeTCP(self , port):
		'''
		Performs data acquisition via TCP protocol
		'''
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(self.timeout)
		serverAddress = ('', port)
		sock.bind(serverAddress)
		sock.listen(1)
		print ('waiting for connection...')
		[connection, clientAddress] = sock.accept()
		connection.setblocking(1)
		print ('connection from ' + str(clientAddress))
		while self.go:
			data = connection.recv(self.bufferSize)
			if not data: break
			self.__notifyListeners(self.__extractSensorData(data.decode("utf-8")))
		connection.close()


	def executeUDP(self , port):
		'''
		Performs data acquisition via UDP protocol
		'''
		UDPSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
		UDPSocket.settimeout(self.timeout)
		serverAddress = ('', port)
		print('Listening on port ' + str(port))
		UDPSocket.bind(serverAddress)
		while self.go:
			[data,attr] = UDPSocket.recvfrom(self.bufferSize)
			if not data: break
			self.__notifyListeners(self.__extractSensorData(data.decode("utf-8")))
		UDPSocket.close()
			
	@staticmethod
	def strings2Floats(listString):
		'''
		Converts a list of Strings to a list of floats; returns the converted list 
		'''
		out=[]		
		for j in range(0, len(listString)):
			if(listString[j]!=''):
				out.append( float(listString[j]))
		return out
		
	@staticmethod
	def printSensorsData (sensorData):		
		'''
		Prints to console the acquired sensors'data 
		'''
		sensor_name= " "
		key = " "
		val = " "
		sensor_dict = {}
		value_dict = {}
		gps_dict = {}
		accl_dict = {}
		gyro_dict = {}
		grav_dict = {}
		linaccel_dict = {}
		vect_dict = {}
		magnet_dict = {}
		baro_dict = {}

		try:	
			for acquisition in sensorData:
				i = 1;
				for sensorAcq in acquisition :
					sensor_num = 'Sensor' + str(i)
					for index in range(len(sensorAcq)):
						if(i!=7):
							sensor_dict = HIMUServer.sensor_key(i,sensorAcq[index],sensor_dict,value_dict,index,accl_dict,gyro_dict,grav_dict,vect_dict,magnet_dict,linaccel_dict,baro_dict) #do not change this to value_dict unless a result to fix that has arise. Or else face awkward ass wrath
						else:
							if(index == 0):
								key = "Lat."
							elif(index == 1):
								key = "Lon."
							elif(index == 2):
								key = "Alt."
							gps_dict[key] = float(sensorAcq[index])
							sensor_dict["GPS"] = gps_dict
					i+=1
				json_dict = json.dumps(sensor_dict,indent = 2)
				print(type(json_dict))
				json_file = open("test.json","a")
				json.dump(json_dict,json_file,indent = 2)
				json_file.write("\n")
				time.sleep(2)
		except Exception as ex:
			print("done")
			json_file.close()
			print(str(ex))

	@staticmethod
	def sensor_key(i,num,sensor_dict,val_dict,index,accl_dict,gyro_dict,grav_dict,vect_dict,magnet_dict,linaccel_dict,baro_dict):
		if(i == 1):
			name = "Accelerometer"
			key = HIMUServer.sensor_val(name,index)
			accl_dict[key] = float(num)
			sensor_dict[name] = accl_dict
		elif(i==2):
			name = "Gyroscope"
			key = HIMUServer.sensor_val(name,index)
			gyro_dict[key] = float(num)
			sensor_dict[name] = gyro_dict
		elif(i==3):
			name = "Gravity"
			key = HIMUServer.sensor_val(name,index)
			grav_dict[key] = float(num)
			sensor_dict[name] = grav_dict
		elif(i==4):
			name = "Linear Acceleration"
			key = HIMUServer.sensor_val(name,index)
			linaccel_dict[key] = float(num)
			sensor_dict[name] = linaccel_dict
		elif(i==5):
			name = "Rotation Vector"
			key = HIMUServer.sensor_val(name,index)
			vect_dict[key] = float(num)
			sensor_dict[name] = vect_dict
		elif(i==6):
			name = "Magnetometer"
			key = HIMUServer.sensor_val(name,index)
			magnet_dict[key] = float(num)
			sensor_dict[name] = magnet_dict
		return sensor_dict

	@staticmethod
	def sensor_val(name,i):
		key = ""
		if(i == 0):
			key = name + ".X"
		elif(i ==1):
			key = name + ".Y"
		elif(i==2):
			key = name + ".Z"
		return key

				
	def __extractSensorData (self, dataString):		
		'''
		Extracts sensors'data from the input raw data string.
		The return object is an array of arrays [i][j], where i corresponds to sampled acquisitions and j corresponds to sensors' value.
		All sensors' values are represented as strings.
		'''
		packages = dataString.split(self.packSeparator)
		retVal = []
		for pack in packages:
			if pack!='' :
				try:
					packVal = []
					packSplit = pack.replace('\n', '').replace('\r', '').split(",")
					numSensors = int(math.floor( len(packSplit)  / valuesPerSensor))
					lFloat = HIMUServer.strings2Floats(packSplit)
					for i in range(0 , numSensors):
						p = packSplit[i*valuesPerSensor : (i+1)*(valuesPerSensor)]
						packVal.append(p)
					if(len(packVal)>0):
						retVal.append(packVal)
				except Exception as ex:
					pass
		return retVal


	def start(self, protocol, arg):
		'''
		Executes the data acquisition;
		<protocol> 	the supported protocol: 'UDP' , 'TCP' , 'FILE' o 'RAW'
		<arg> 		the port number in case of UDP or TCP protocols, input file path in case of 'FILE' protocol
		'''
		print('protocol: ' + protocol)
		try:
			if protocol == 'JSON':
				self.executeTCP(int(arg))
			elif protocol == 'TCP':
				self.executeTCP(int(arg))
			elif protocol == 'UDP':
				self.executeUDP(int(arg))
		except Exception as ex:
			print(str(ex))
			
	def stop(self ):
		self.go = false
		