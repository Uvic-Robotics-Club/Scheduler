#!/usr/bin/python
import shelltypes
from shelltypes import Vector3

import traceback, socket, json, _thread


#Takes a JSON packet and converts it into Vector3s
#(since all the phone sensors have 3 dimensions)
#For now, this just prints the Vector3s
#Figure out how to REALLY process them later
def splitPublish(json_raw):
    if len(json_raw) != 0:
            #Converting a JSON object into a Python dictionary
            decoded = json.loads(json_raw)
            #print(decoded)

            #3D vector that will temporarily contain all 3D data
            #before it is published
            trio = Vector3()

            for hyperIMUSensor in [key for key, val in sensorDict.items()]:
                if hyperIMUSensor in decoded:
                    trio.x = float(decoded[hyperIMUSensor][0])
                    trio.y = float(decoded[hyperIMUSensor][1])
                    trio.z = float(decoded[hyperIMUSensor][2])
                    print(trio)

                    #Still can use the sensorDict values (strings) to figure out where everything is going later

if __name__ == '__main__':

    #An example json packet for testing purposes
    dummyjson = '{"K330 3-axis Accelerometer": [-0.02214636653661728, 8.012794494628906, 6.174646377563477], "os": "hyperimu", "GPS": [48.46910729, -123.31144137, 41]}'

    #A dictionary that maps HyperIMU's sensor names to more coherent names
    sensorDict = {}
    sensorDict["K330 3-axis Accelerometer"] = "PhoneAccel"
    sensorDict["GPS"] = "PhoneGPS"

    splitPublish(dummyjson)
