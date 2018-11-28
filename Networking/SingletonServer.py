import socket
from time import sleep


class Station_Communication_Gate():
    class_connection_list = []
    #  class_connection_list --> [server socket Object , ip , port , client connected to the server , address of client connected to the server ]

    def __init__(self, ip, port):
        if (self.class_connection_list == []):  #checks if server is listening
            self.class_connection_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))  # creating a server
            # ... and storing it in index 0 of class_connection_list
            self.class_connection_list.append(ip)  # storing ip in index 1
            self.class_connection_list.append(port)  # storing port in index 2
            self.class_connection_list[0].bind((ip, port))  # binding the server to the address(ip, port)
            self.class_connection_list[0].listen(1)  # server starts listening
            print("Server started listening:", ip, ":", port)

            client, clientAddress = self.class_connection_list[0].accept()
            self.class_connection_list.append(client)  # storing the client that has connected to the server in
            # ... index 3 of class_connection_list
            self.class_connection_list.append(clientAddress)  # storing the address of the client that has connected to
            # ... the server in index 5 of class_connection_list
            print("Got a connection from", clientAddress[0], ":", clientAddress[1])
        else:  # this else statement runs if an instance of the class exists already
            pass


    def send(self, msg): # it is used to send data to client
        try:  # tries sending data to server
            self.class_connection_list[3].send(bytes(msg, encoding='utf-8'))

        except socket.error:  # this error is raised if client disconnects
            print("Client disconnected")
            print("Waiting for client to reconnect...")
            client, clientAddress = self.class_connection_list[0].accept() # getting connection from (new) client again
            print("Client successfully reconnected")
            self.class_connection_list[3] = client  # storing the new client in index 3 of class_connection_list
            self.class_connection_list[4] = clientAddress  # storing the address of the new client in index 4 of
            # ... class_connection_list


    def receive(self):
        try:
            client_message = self.class_connection_list[3].recv(1024)  # using socket module to receive data from server

        except socket.error: # this error is raised if client disconnects
            print("Client disconnected")
            print("Waiting for client to reconnect...")
            client, clientAddress = self.class_connection_list[0].accept()  # getting connection from (new) client again
            print("Client successfully reconnected")
            self.class_connection_list[3] = client  # storing the new client in index 3 of class_connection_list
            self.class_connection_list[4] = clientAddress  # storing the address of the new client in index 4 of
            # ... class_connection_list
        else:  # runs only if no exception has been raised
            return client_message


def main():
    ip = socket.gethostbyname(socket.gethostname())  # Getting ip address of the computer
    port = 9999  # setting port to 9999
    gateS = Station_Communication_Gate(ip, port)
    gateS2 = Station_Communication_Gate("QQQQQQQQ", 27477774774)

    while(True):
        data  = gateS.receive()
        print(data)

        if (data == bytes("Hello server", encoding='utf-8')):
            sleep(1)
            gateS.send("Hello to client")
        elif (data == bytes("disconnect", encoding='utf-8')):
            sleep(1)
            gateS.send("GoodBye")
            #client.close()
            break
        else:
            sleep(1)
            gateS2.send("DUUUUUUUDDDEEE YOU DID ITTTT!!!!!")






if __name__ == '__main__':
    main()