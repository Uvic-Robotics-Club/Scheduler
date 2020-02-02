import socket
from time import sleep
import queue
from threading import Thread
import errno

# todo: be aware that messages that are failed to be sent due to a failure, are added to the end of the queue, so it
#  takes them a while to reach the server
# todo: there are a lot of 'sleep' commands in this program; these are there to enable the user to see the output of
#  the programme and make sure of the correct functionality. However, while using the class for actual purposes, these
#  should be commented out

class Rover_Communication_Gate:
    class_connection_list = [None, None, None]  # class_connection_list --> [client socket Object, ip of server, port]
    sending_queue = queue.Queue()  # a queue that contains all the data that needs to be sent to the station
    # ... since this is a complex object, it is shared among all instances of the class

    socketObject = 0
    serverIP = 1
    port = 2
    UDPBroadcastPort = 9999
    UDPReceivePort = 2048
    MSGreceivePort = 1024
    initialPort = 6663


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

    def __init__(self):
        if (self.class_connection_list == [None, None, None]):  # checks if no connection exists

            self.class_connection_list[self.port] = self.initialPort

            # connection will be established in the thread
            t = Thread(target=self.main_thread)
            t.start()  # starting the main thread
        else:
            # if this else is run, it means that there already exists a connection with the server. So it does not do
            # ~ anything and hence, further objects will use the already existing connection. (ie; this brings a
            # ~ singleton behaviour to this class
            pass



    def connectUDP(self):
        """
        First we create a UDP client so it can broadcast to all the servers in the network. The intention of doing so is
        to find the ip address of the server. After this objective is achieved, we establish a tcp connection between
         the two devices,
        """

        UDP_client_address = ('<broadcast>', self.UDPBroadcastPort)
        UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #  UDP client used to broadcast to server
        UDP_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # this function is called so this object uses
        # ~ UDP protocol

        UDP_client.settimeout(1)

        connected_to_UDP_server = False
        while connected_to_UDP_server == False:
            try:
                UDP_client.sendto(bytes("A", encoding='utf-8'), UDP_client_address)
                """
                After broadcasting, if the expected server to listen is listening, it will respond to the letter 'A' 
                with a letter 'B'. in that case we know that the server and the client have found each other. Which 
                means that we will have the ip address of the server and then we can establish a TCP connection with the
                server. This ip address could be found in the 1st index of the tuple 'server_addr'
                """
                recv_data_from_server, server_addr = UDP_client.recvfrom(self.UDPReceivePort)
                msg = recv_data_from_server.decode('utf-8')

                if msg == "B":
                    IP_ADDRESS_OF_SERVER = server_addr[0]
                    self.class_connection_list[self.serverIP] = IP_ADDRESS_OF_SERVER
                    connected_to_UDP_server = True
                    recv_port_from_server, server_addr = UDP_client.recvfrom(self.UDPReceivePort)
                    port_from_server = recv_port_from_server.decode('utf-8')
                    self.class_connection_list[self.port] = int(port_from_server)
                    print("the port from server is: " + str(self.class_connection_list[self.port]))

            except socket.timeout:
                print(" UDP Server not listening")
                connected_to_UDP_server = False

    def connectTCP(self):

        # ================= Establishing the TCP connection below this line ===========================


        connectedToServer = False  # indicates if client socket client is connected to server
        while (connectedToServer == False):
            try:  # program tries to connect to server
                client = socket.socket()  # creating client object
                address = (self.class_connection_list[self.serverIP], self.class_connection_list[self.port])  # creating address tuple
                client.connect(address)  # connecting to the server using address
                connectedToServer = True  # assuming that the client has successfully connected to the server and
                # ~ hence,changing the boolean accordingly (if connecting fails or , the exception clause below will run
            except ConnectionRefusedError:  # This exception is raised if the server is not listening
                connectedToServer = False # since there is no server, we change the boolean back to false
                print("(refused) Server not listening...")
                print(self.class_connection_list[self.port])
                #print(IP_ADDRESS_OF_SERVER)
                sleep(1)
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # since there has been a failed connection
                # ~ for the previous client object, something has changed inside it and hence, it can not try to
                # connect again. So we create a new client object.


            except ConnectionResetError:
                connectedToServer = False  # since there is no server, we change the boolean back to false
                print("(reset) Server not listening...")
                sleep(1)
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # since there has been a failed connection
                # ~ for the previous client object, something has changed inside it and hence, it can not try to
                # connect again. So we create a new client object.

                # client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


        self.class_connection_list[self.socketObject] = client
        self.class_connection_list[self.socketObject].settimeout(0.5)  # setting a time out for the thread so it doesn't spend time on
        # ~ the task for more than 0.5 seconds; so if it doesn't receive anything for 0.5 seconds, it stops trying to
        # ~ receive sth from client and starts sending stuff, if there are any

        return client  # returning client, which is a socket object

    def connectToServer(self): # creates a client and connects it to the server
        self.connectUDP()
        self.connectTCP()

    def send(self, msg):  # it is used to send data to server
        self.sending_queue.put(msg + "\n")  # adding the message to the class sending  queue

    def main_thread(self):  # this is the main thread of the client which is pointed to in the initializer
        self.connectToServer()
        while True:
            try:
                msg = (self.class_connection_list[self.socketObject].recv(self.MSGreceivePort)).decode("utf-8")
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
                if error == errno.ECONNRESET:
                    # "ECONNRESET" is the exception that is raised when the other end is disconnected. In this case,
                    # ... this error is raised if server disconnects
                    print("Server disconnected while trying to receive data from server")
                    sleep(1)
                    self.connectToServer()

            else:
                for item in msg:
                    print(item)  # todo: this print statement must be changed to a function call to merge with the shell
                    # todo: (only for UVic Robotics use)

            for counter in range(10):  # sending 10 messages to the station
                if self.sending_queue.empty():
                    break
                else:
                    try:
                        currentMsgToSend = self.sending_queue.get()   # storing the msg that is about to be sent so if
                        # ... the client fails to send it, it gets added to the queue and is not lost
                        self.class_connection_list[self.socketObject].send(bytes(currentMsgToSend, encoding='utf-8'))
                        # print("DATA WAS SENT TO SERVER")
                    except socket.error:
                        self.sending_queue.put(currentMsgToSend)
                        print("Server disconnected while trying to send data to server")
                        sleep(1)
                        self.connectToServer()


# The below "main" is written to demonstrate the functionality

# The main function is only written to test the class. It is not necessary to have it.
def main():
    gate = Rover_Communication_Gate()
    gate2 = Rover_Communication_Gate()
    gate3 = Rover_Communication_Gate()

    for i in range(10000):
        gate.send(str(i))
        sleep(1)


if __name__ == '__main__':
    main()