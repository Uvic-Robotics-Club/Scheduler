HIMU-Server
===========

HIMU Server (HyperIMU Server) is a python library covering all server-side stream protocols supported by [HyperIMU](https://ianovir.com/works/mobile/hyperimu/). It performs basic operations such as input stream reading and csv sequence chunking.

Read the [HyperIMU Documentation](https://ianovir.com/works/mobile/hyperimu/hyperimu-help/) for more details.

# Overview #

## Network configurations ##

In order to connect the HIMUServer application and the HyperIMU app, you need the following:

* Be sure the Android device (HyperIMU client) and you server (HIMUServer) are connected to the **same network**
* Press on the 3 lines on the top left corner of the app and press settings to configure the HyperIMU app with the server **IP address** and **server port**
* Be sure the **firewall** in the server machine doesn't limit the server application 
* (On Mac) If obtain `socket.error: [Errno 48] Address already in use ` execute the following command:
```
Find the port that's being used (eg. 2055)
sudo lsof -i:port_number

kill XXXX
```

## Smartphone Configuration ##
Smartphone Used to Test the App: Huawei P20 Pro (Note: will be changed to Motorola Nexus 6)

In order to configure the HyperIMU app to send the desired sensor to a remote server:
 * Download the HyperIMU App onto your android device
 * Follow the network configuration guide
 * Click the settings menu and change the stream protocol to TCP
 * To get GPS data, click the settings menu and within the Trailer button, slide the GPS slider to the right
 * To get desired sensor data, click the sensor list menu and select the desire sensors (Note: Choose only the uncalibrated sensor if its the only option, otherwise avoide it to have better precision in data collection)
 * The order of the data that the sensor sends to the server is from top to bottom

## Sensor List (More could be added) ## 
Sensor Specification (P20 Pro): 
* Rotation Vector
* Gravity
* Accelerometer
* GPS
* Gyroscope
* Linear Acceleration
* Magnetometer

Sensor Specification (Nexus 6):
* Rotation Vector
* Gravity
* Accelerometer
* GPS
* Gyroscope
* Barometer
* Linear Acceleration
* Magnetometer


## Protocols and Data Format ##

HyperIMU streams the sensors' data by using the protocols UDP and TCP,
or by storing them into a file for an offline processing.
The order of the sensors is the same as specified in the HyperIMU's settings.
However, for this project, only TCP protocol would be used. 


**GPS Data** (Latitude,Longitude, Altitude) are added to the very end of the data stream 
**Timestampe** , **MAC Address** , and **GPS NMEA** will be implemented in a future update


## Launching the server ##

Launch the server with TCP protocol:
```python
	myHIMUServer.start("TCP", 2055)
```

UDP protocol:
```python
	myHIMUServer.start("UDP", 2055)
```

Take a look to the `demo.py` file for more info.

# For more details about the HyperIMU app 
visit https://github.com/ianovir/HIMUServer

# Things Used:
Python Version: 3.7.4
Library: https://github.com/ianovir/HIMUServer

# Copyright
Copyright(c) 2019 Sebastiano Campisi - [ianovir.com](https://ianovir.com). 
Read the LICENSE file for more details.


