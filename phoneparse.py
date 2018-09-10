#!/usr/bin/python
import shelltypes
from shelltypes import Vector3

import traceback, socket, json, _thread


#Takes a JSON packet and converts it into Vector3s
#(since all the phone sensors have 3 dimensions)
#For now, this just prints the Vector3s
#Figure out how to REALLY process them later
#This function should only update the database class
def splitPublish(json_raw):
    if len(json_raw) != 0:
            #Converting a JSON object into a Python dictionary
            decoded = json.loads(json_raw)
            #print(decoded)

            #3D vector that will temporarily contain all 3D data
            #before it is published
            trio = Vector3()

            #Let's publish from all the desired sensors!
            #The list ccomprehension allows us to sift through the JSON packet
            #and find the desired HyperIMU data
            #because we stored the data stream names in sensorDict in the main
            for hyperIMUSensor in [key for key, val in sensorDict.items()]:
                if hyperIMUSensor in decoded:
                    trio.x = float(decoded[hyperIMUSensor][0])
                    trio.y = float(decoded[hyperIMUSensor][1])
                    trio.z = float(decoded[hyperIMUSensor][2])
                    print(trio)

                    #Still can use the sensorDict values (strings) to figure out where everything is going later

#We need an object that is a bundle of Vector3s being continually update by splitPublish
#Alternative: have splitPublish call all the methods that deal directly with the JSON data. Not good.
#So we are going to want a data logger class
#The data logger class will be mostly a bundle of Vector3s being continually replaced and also keeping logs of misc data
#When the data logger class is updated, it needs to know what to alert

#This function is run on multiple threads
#It accepts HyperIMU information and calls splitPublish
def clientrun(clientsocket, address):
    while True:
        try:
            message = clientsocket.recv(8192)
            splitPublish(message)
        except Exception as e:
            traceback.print_exc()
            print(e)
    clientsocket.close()


def tcp_receive():
    host = ''
    port = 5555

    #TCP connection! HyperIMU can only send JSON over TCP, not UDP
    #put this block into a loop so that any disconnection will shut everything down
    #and then resume listening
    s = socket.socket()
    s.bind((host, port))
    print('Waiting for connection...')
    s.listen(1)
    while(1):
        try:
            c, addr = s.accept()
            print("Connection received!")
            _thread.start_new_thread(clientrun,(c,addr))
        except Exception as e:
            traceback.print_exc()
            print(e)

if __name__ == '__main__':

    #An example json packet for testing purposes
    dummyjson = '{"K330 3-axis Accelerometer": [-0.02214636653661728, 8.012794494628906, 6.174646377563477], "os": "hyperimu", "GPS": [48.46910729, -123.31144137, 41]}'

    #A dictionary that maps HyperIMU's sensor names to more coherent names
    sensorDict = {}
    sensorDict["K330 3-axis Accelerometer"] = "PhoneAccel"
    sensorDict["GPS"] = "PhoneGPS"

    #Uncomment this to just test the splitPublish function
    #splitPublish(dummyjson)

    tcp_receive()
