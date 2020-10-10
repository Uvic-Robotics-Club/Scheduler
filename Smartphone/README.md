# Smartphone 

This directory contain programs that extract embedded sensors from a Smartphone using the [HyperIMU Library](https://ianovir.com/works/mobile/hyperimu/hyperimu-help/) and writing those data into a JSON file. The data is being transmitted via TCP signal from the smartphone to a server (i.e. computer) at an elsewhere location. This directory uses 2 programs (phone_client and extractSensorData) to extract sensor data in an xyz format for applicable sensors. Exceptions include Timestamp where only one value is extracted and GPS where its lat/long/alt values are extracted.

Example of a sample file output:
{Timestamp: {Timestamp:123456789}, Accelerometer:{x:123,y:234,z:345}, GPS:{lat:123,long:234,alt:456}} 

File Descriptions:
The directory,HIMUServer, is a slightly modified copy of the original library code.

phone_client.py converts sensor data into JSON Object and writes them into a file

extractSensorData.py extracts sensor data from the smartphone and sends it to phone_client.py