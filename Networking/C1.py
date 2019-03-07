#UDP client broadcasts to server(s)
from time import sleep
import socket

address = ('<broadcast>', 54545)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


connectedToServer = False
while connectedToServer == False:
    try:

        client_socket.sendto(bytes("A", encoding='utf-8'), address)
        client_socket.settimeout(1)

        recv_data, addr = client_socket.recvfrom(2048)  #addr would be address of server

        #print(addr, recv_data)
        msg = recv_data.decode('utf-8')
        print (msg)

        if msg == "B":
            connectedToServer = True


    except socket.timeout:
        print ("Server not listening")




