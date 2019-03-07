#UDP server responds to broadcast packets
#you can have more than one instance of these running


import socket
from time import sleep


address = ('', 54545)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)

roverConnected = False
while roverConnected ==False:
    print ("Listening")
    recv_data, addr = server_socket.recvfrom(2048)  # addr would be address of client
    msg = recv_data.decode('utf-8')
    print (msg)

    if (msg == "A"):
        server_socket.sendto(bytes("B", encoding='utf-8'), addr)
        roverConnected = True
        print (addr)

    else:
        server_socket.sendto(bytes("*", encoding='utf-8') + recv_data, addr)


