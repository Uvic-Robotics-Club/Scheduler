from HIMUServer.HIMUServer import HIMUServer
import json


SENSOR_NAME = ["Accelerometer","Magnetometer","Gyroscope","Gravity","Linear Acceleration","Rotation Vector","GPS"] #for model Huawei P20 Pro
#can create another SENSOR_NAME list for another smartphone


class SmartphoneListener:
    def __init__(self,serverInstance):
        self.__server = serverInstance
    def notify (self, sensorData):
        self.convertDataSensor(sensorData)
    
    @staticmethod
    def convertDataSensor(sensor_packets):
        '''
        Converts sensor data into JSON Object/String and writes the data to a file
        '''
        try:
            sensor_dict = {}
            for sensor_packet_list in sensor_packets: #sensorData is a huge packet of multiple sensor_data_lists with each sensor_data_list containing one sensor_set
                sensor_name_index = 0
                sensor_name = SENSOR_NAME[sensor_name_index]
                sensor_dict[sensor_name] = {}
                for sensor  in sensor_packet_list:
                    sensor_name = SENSOR_NAME[sensor_name_index]
                    if sensor_name == "GPS":
                        sensor_dict[sensor_name] = {"lat":float(sensor[0]),"long":float(sensor[1]),"alt":float(sensor[2])}
                    else:
                        sensor_dict[sensor_name] = {"x":float(sensor[0]),"y":float(sensor[1]),"z":float(sensor[2])}
                    sensor_name_index+= 1
                json_dict = json.dumps(sensor_dict,indent = 2) #indent here provides horizontal indent when writing data to the file
                json_file = open("output.json","a")
                json.dump(json_dict,json_file,indent = 2) #provides horizontal indent when writing json_object to file
                json_file.write("\n")
        except Exception as err:
            print(str(err))
#HIMUServer Instance
myHIMUServer = HIMUServer()

#Creating listener and adding it to the server instance:
myListener = SmartphoneListener(myHIMUServer)
myHIMUServer.addListener(myListener)


#Change the timeout (in seconds) :
myHIMUServer.timeout = 2

#Launch acquisition via TCP on port 2055:
myHIMUServer.start("TCP", 2055)

#Launch acquisition via UDP on port 2055:
myHIMUServer.start("UDP", 2055)