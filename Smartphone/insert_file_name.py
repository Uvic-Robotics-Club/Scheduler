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
        try:
            for acquisition in sensorData:
                i = 1
                # sensor_dict["Sensor" + str(i) + ": "] = {}
                if(i == 1):
                    name = "Timestamp"
                elif(i == 2):
                    name = "Accelerometer"
                elif(i == 3):
                    name = "Magnetometer"
                elif(i == 4):
                    name = "Gyroscope"
                elif(i == 5):
                    name = "Gravity"
                elif(i==6):
                    name = "Linear Acceleration"
                elif(i==7):
                    name = "Rotation Vector"
                elif(i==8):
                    name = "GPS"
                sensor_dict[name + ": "] = {}
                for sensorAcq  in acquisition:
                    if(name == "Timestamp"):
                        sensor_dict[name + ": "] = {"Data: ":float(sensorAcq[0])}
                    elif( name == "GPS"):
                        sensor_dict[name +": "] = {"lat: ":float(sensorAcq[0]),"long: ":float(sensorAcq[1]),"alt: ":float(sensorAcq[2])}
                    else:
                        sensor_dict[name + ": "] = {"x":float(sensorAcq[0]),"y":float(sensorAcq[1]),"z":float(sensorAcq[2])}
                    i+= 1
                json_dict = json.dumps(sensor_dict,indent = 2)
                json_file = open("test88.json","a")
                json.dump(json_dict,json_file,indent = 2)
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