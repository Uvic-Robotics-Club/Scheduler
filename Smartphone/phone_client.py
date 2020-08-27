from HIMUServer.HIMUServer import HIMUServer
import json

# For model Huawei P20 Pro
SENSOR_NAME = ["Timestamp","Accelerometer","Magnetometer","Gyroscope","Gravity","Linear Acceleration","Rotation Vector","GPS"]
#can create another SENSOR_NAME list for another smartphone


class SmartphoneListener:
    def __init__(self,serverInstance):
        self.__server = serverInstance
    def notify(self, sensorData):
        self.convert_DataSensor(sensorData)
    
    @staticmethod
    def convert_DataSensor(sensor_packets):
        '''Converts sensor data into JSON Object/String and writes the data to a file

        sensor_packets is a huge packet of multiple sensor_data_lists with each sensor_data_list containing one sensor_set
        '''
        try:
            sensor_dict = {}
            for sensor_packet_list in sensor_packets:
                sensor_name_index = 0
                sensor_dict["Timestamp"] = {}
                for sensor in sensor_packet_list:
                    sensor_name = SENSOR_NAME[sensor_name_index]
                    if sensor_name == "Timestamp":
                        sensor_dict["Timestamp"] = {"Timestamp": float(sensor[0])}
                    elif sensor_name == "GPS":
                        sensor_dict["GPS"] = {"lat":float(sensor[0]),"long":float(sensor[1]),"alt":float(sensor[2])}
                    else:
                        sensor_dict[sensor_name] = {"x":float(sensor[0]),"y":float(sensor[1]),"z":float(sensor[2])}
                    sensor_name_index += 1
                json_dict = json.dumps(sensor_dict)
                json_file = open("Smartphone/phone_sensor_data9.json","a")
                json.dump(json_dict, json_file)
                json_file.write("\n")
        except Exception as err:
            pass
            # Below statement commented because of errors coming from smartphone not sending enough sensor_values to console, no effect on performance(anything)
            #print(str(err))

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