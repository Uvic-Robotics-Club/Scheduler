#import HIMUServer.HIMUServer will spit out module error
from HIMUServer.HIMUServer import HIMUServer
import json

#HIMUServer instance:

class SmartphoneListener:
    def __init__(self,serverInstance):
        self.__server = serverInstance
    def notify (self, sensorData):
        self.convertDataSensor(sensorData)
    
    @staticmethod
    def convertDataSensor(sensorData):
        '''
        Converts sensor data into JSON Object/String and writes the data to a file
        '''
        name = ""
        sensor_dict = {}
        SENSOR_NAME = ["Timestamp","Accelerometer","Magnetometer","Gyroscope","Gravity","Linear Acceleration","Rotation Vector","GPS"] #for model Huawei P20Pro
        #can create another SENSOR_NAME list for another smartphone
        try:
            for sensor_data_list in sensorData: #should understand what ytpe of data structure is being passed through as "sensorData" to this method
                sensor_name_index = 0
                sensor_name = SENSOR_NAME[sensor_name_index]
                sensor_dict[sensor_name] = {}
                for sensorAcq  in sensor_data_list:
                    sensor_name = SENSOR_NAME[sensor_name_index]
                    if sensor_name == "Timestamp":
                        sensor_dict[sensor_name] = {"Data":float(sensorAcq[0])}
                    elif sensor_name == "GPS":
                        sensor_dict[sensor_name] = {"lat":float(sensorAcq[0]),"long":float(sensorAcq[1]),"alt":float(sensorAcq[2])}
                    else:
                        sensor_dict[sensor_name] = {"x":float(sensorAcq[0]),"y":float(sensorAcq[1]),"z":float(sensorAcq[2])}
                    sensor_name_index+= 1
                json_dict = json.dumps(sensor_dict,indent = 2) #indent here provides horizontal indent
                json_file = open("test89.json","a")
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

#Launch acquisition from local file:
myHIMUServer.start("FILE", "HIMU-filetest.csv")