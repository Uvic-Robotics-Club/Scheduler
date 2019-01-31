import socket
from time import sleep
import queue
from threading import Thread
import errno

# try all the hosts and then connect

class Rover_Communication_Gate:
    class_connection_list = []  # class_connection_list --> [client socket Object, ip, port]
    sending_queue = queue.Queue()  # a queue that contains all the data that needs to be sent to the station
    # ... since this is a complex object, it is shared among all instances of the class

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

            t = Thread(target= self.main_thread)
            t.start()
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
        self.sending_queue.put(msg + "\n")  # adding the message to the class sending  queue

    def main_thread(self):  # this is the main thread of the client which is pointed to in the initializer
        self.class_connection_list[0].settimeout(0.5)  # setting a time out for the thread so it doesn't spend time on
        # ... the task for more than 0.5 seconds; so if it doesn't receive anything for 0.5 seconds, it stops trying to
        # ... receive sth from client and starts sending stuff, if there are any
        while True:
            try:
                msg = (self.class_connection_list[0].recv(1024)).decode("utf-8")  # since tye string was encoded to
                # ... bytes for sending by the server, it has to be decoded now
                msg = msg.split("\n")
                for item in msg:
                    item.strip("\n")

            except socket.timeout:  # catching the timeout error
                print("timeout error while waiting to receive from server")

            except socket.error as error:
                """
                Notice the connection of the initial client object has failed. If we try to create a new object, it will 
                point to the previous object as it is supposed to. However, the previous object is broken and is not 
                working. Hence, we need to completely empty the 'class_connection_list' se when we try to create a new 
                object, the program actually creates a new object.
                """
                if error == errno.ECONNRESET:  # checking if the raised error is "ECONNRESET" type
                    # "ECONNRESET" is the exception that is raised when the other end is disconnected. In this case,
                    # ... this error is raised if client disconnects
                    print("Server disconnected while trying to receive data from server")
                    sleep(1)
                    if self.class_connection_list != []:
                        ip = self.class_connection_list[1]  # storing ip
                        port = self.class_connection_list[2]  # storing port
                        self.cleanConnectionList()
                    self.class_connection_list.append(self.connectToServer(ip, port))  # creating a new client
                    # ... socket object
                    # ...and storing it in the first index of class_connection_list
                    self.class_connection_list.append(ip)  # appending ip to class_connection_list
                    self.class_connection_list.append(port)  # appending port to class_connection_list
                    self.class_connection_list[0].settimeout(0.5)  # timeout has to be reset since it is a new
                    # ... object classConnectionList
            else:
                for item in msg:
                    print(item)

            for counter in range(10):  # this for loop is intended to send 10 messages to the station
                if self.sending_queue.empty():
                    break
                else:
                    try:
                        currentMsgToSend = self.sending_queue.get()   # storing the msg that is about to be sent so if
                        # ... the client fails to send it, it gets added to the queue and is not lost
                        self.class_connection_list[0].send(bytes(currentMsgToSend, encoding='utf-8'))
                        print("DATA WAS SENT TO SERVER")
                    except socket.error:
                        self.sending_queue.put(currentMsgToSend)
                        print("Server disconnected while trying to send data to server")
                        sleep(1)
                        if self.class_connection_list != []:
                            ip = self.class_connection_list[1]  # storing ip
                            port = self.class_connection_list[2]  # storing port
                            self.cleanConnectionList()
                        self.class_connection_list.append(self.connectToServer(ip, port))  # creating a new client
                        # ... socket object
                        # ...and storing it in the first index of class_connection_list
                        self.class_connection_list.append(ip)  # appending ip to class_connection_list
                        self.class_connection_list.append(port)  # appending port to class_connection_list
                        self.class_connection_list[0].settimeout(0.5)  # timeout has to be reset since it is a new
                        # ... object classConnectionList


def main():
    port = 9999  # setting port to 9999
    # Setting up client
    ipOfServer = socket.\
    gethostbyname("")  # getting ip address of the server (this computer for now!)

    gate = Rover_Communication_Gate('<broadcast>', port)

    gate2 = Rover_Communication_Gate("HEEEEYY", 2000000)
    gate3 = Rover_Communication_Gate("YOOOOOO", 900001)

    for i in range(10000):
        gate.send(str(i))


if __name__ == '__main__':
    main()