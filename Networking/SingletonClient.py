import socket
from time import sleep

# add threading

class Rover_Communication_Gate:
    class_connection_list = []  # class_connection_list --> [ client socket Object, ip, port]
    """
    ---     USING A CLASS VARIABLE WHICH RESULTS IN A SINGLETON BEHAVIOUR FOR THE CLASS  ---
    having a "connection" or "client socket object" as a class variable which is SHARED among all objects and is not 
    reset after a new instance of the class is created, would be operating just like a singleton class.
    There are two types of objects in python: simple and complex. when a simple object is reused, it is copied to a
    new memory location and used, and this is done because the object is simple and it is easy to copy the object. Such
    objects are strings, integers, and booleans. 
    When a complex object is reused, the programmer just uses a pointer to point to the same memory location.
    Hence, any changes made to that memory location, would affect all other objects that are using that pointer.
    As a result, if we use a complex object like a list as a class variable, its going to be declared only once and 
    would result in a singleton behaviour for this class.
    """
    def __init__(self, ip, port):
        if  (self.class_connection_list == []):  # checks if no connection exists

            self.class_connection_list.append(self.connectToServer(ip, port)) # creating a socket client object and
            # ... storing it in the first location of the 'class_connection_list'
            self.class_connection_list.append(ip)  # storing the ip in second location of the list
            self.class_connection_list.append(port)  # storing the port in second location of the list
            """
            Notice that it is necessary to APPEND to the list and not redefine it. because if we redefine,
            the program will start using a new memory location and this stops the class from having a singleton
            behaviour
            """
        else:
            # if this else is run, it means that there already exists a connection with the server. So it does not do
            # ... anything and hence, further objects will use the already existing connection
            pass


    def connectToServer(self, ip, port): # creates a client and connects it to the server
        # "ip" is the ip of the server that this client is trying to connect to

        connectedToServer = False  # Defining a boolean to show whether client is connected to server
        while (connectedToServer == False):  # trying to connecting the client to the server while it is not connected
            try:  # program tries to connect to server
                client = socket.socket()  # creating client object
                address = (ip, port)  # creating address tuple
                client.connect(address)  # connecting to the server using address
                connectedToServer = True  # assuming that the client has successfully connected to the server and
                # ... hence,changing the boolean accordingly (if connecting fails or , the exception clause below will run
            except ConnectionRefusedError:  # This exception is raised if the server is not listening
                connectedToServer = False # since there is no server, we change the boolean back to false
                print("Server not listening...")
                sleep(1)
                client = socket.socket()  # since there has been a failed connection for the previous client object,
                # ...something has changed inside it and hence, it can not try to connect again. So we create a new
                # client object.

        return client  # returning client, which is a socket object


    def cleanConnectionList(self):  # this method is used to empty the list when the server stops listening

        for counter in range(3):
            del self.class_connection_list[0]


    def send(self, msg):  # it is used to send data to server
        try: # trying to send the data
            self.class_connection_list[0].send(bytes(msg, encoding='utf-8'))
        except socket.error:  # this exception is raised if server disconnects and hence we can't send data
            """
            Notice the connection of the initial client object has failed. If we try to create a new object, it will 
            point to the previous object as it is supposed to. However, the previous object is broken and is not 
            working. Hence, we need to completely empty the 'class_connection_list' se when we try to create a new 
            object, the program actually creates a new object.
            """
            # hence we should create a new client socket object
            sleep(1)
            if self.class_connection_list != []:
                ip = self.class_connection_list[1]  # storing ip
                port = self.class_connection_list[2]  # storing port
                self.cleanConnectionList()
            self.class_connection_list.append(self.connectToServer(ip, port))  # creating a new client socket object
            # ...and storing it in the first index of class_connection_list
            self.class_connection_list.append(ip)  # appending ip to class_connection_list
            self.class_connection_list.append(port)  # appending port to class_connection_list


    def receive(self):  # it is used to receive messages from server. It returns the data receive
        try:
            server_message = self.class_connection_list[0].recv(1024)  # using socket module to receive data from server

        except socket.error:
            sleep(1)
            if self.class_connection_list != []:
                ip = self.class_connection_list[1]  # storing ip
                port = self.class_connection_list[2]  # storing port
                self.cleanConnectionList()
            self.class_connection_list.append(self.connectToServer(ip, port))  # creating a new client socket object
            # ...and storing it in the first index of class_connection_list
            self.class_connection_list.append(ip)  # appending ip to class_connection_list
            self.class_connection_list.append(port)  # appending port to class_connection_list
        else:  # runs only if no exception has been raised
            return b"[Station]: " + server_message


def main():
    port = 9999  # setting port to 9999
    # Setting up client
    ipOfServer = socket.gethostbyname(socket.gethostname())  # getting ip address of the server (this computer for now!)
    gate = Rover_Communication_Gate(ipOfServer, port)
    gate2 = Rover_Communication_Gate("HEEEEYY", 2000000)
    gate3 = Rover_Communication_Gate("YOOOOOO", 900001)

    while(True):
        gate.send("Hello server")
        gate2.send("2 is working")
        gate3.send("333333")

        print(gate3.receive())


if __name__ == '__main__':
    main()