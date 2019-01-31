#UDP client broadcasts to server(s)
import socket

address = ('<broadcast>', 54545)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Request"
client_socket.sendto(bytes(data, encoding='utf-8'), address)
while True:
    recv_data, addr = client_socket.recvfrom(2048)
    print (addr,recv_data)