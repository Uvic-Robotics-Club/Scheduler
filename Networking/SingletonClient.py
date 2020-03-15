import socket
from time import sleep
import queue
from threading import Thread
import errno

# TODO: be aware that messages that are failed to be sent due to a failure, are added to the end of the queue, so it
#  takes them a while to reach the server
# TODO: there are a lot of 'sleep' commands in this program; these are there to enable the user to see the output of
#  the programme and make sure of the correct functionality. However, while using the class for actual purposes, these
#  should be commented out
# TODO: test singleton behaviour

class Connection:
    def __init__(self, client_socket_object=None, ip=None, port=None):
        self.client_socket_object = client_socket_object
        self.ip = ip
        self.port = port


class Rover_Communication_Gate:

    # the 'connection' variable is shared among all instances of this class. Thus, it could be use to give this class a
    # ~ singleton behaviour
    connection = None

    sending_queue = queue.Queue()  # a queue that contains all the data that needs to be sent to the station
    # ~ since this is a complex object, it is shared among all instances of the class

    UDP_BROADCAST_PORT = 9999
    UDP_RECEIVE_PORT = 2048
    MSG_RECEIVE_PORT = 1024
    INITIAL_PORT = 6663


    def __init__(self):
        # checking if if no connection exists; ie. checks if an instance of the class has not been previously created
        if (self.connection == None):
            print("CREATING AN OBJECT")

            """
            EXTREMELY IMPORTANT: 
            Note the syntax below. Writing 'Rover_Communication_Gate.connection' instead of 'self.connection'
            results in singleton behaviour. 
            DO NOT CHANGE THE SYNTAX!
            
            """
            Rover_Communication_Gate.connection = Connection(port=self.INITIAL_PORT)
            t = Thread(target=self.main_thread)  # connection will be established in the thread
            t.start()

        else:
            # An instance of this class has been previously created; nothing happens
            pass


    """
    A UDP client is required to broadcast to all servers in the network. This function finds the address of the correct
    server.
    """
    def connect_udp(self):

        udp_client_address = ('<broadcast>', self.UDP_BROADCAST_PORT)
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP client used to broadcast to server
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # makes UDP client object use UDP protocol

        udp_client.settimeout(1)

        udp_connected = False
        while udp_connected == False:
            try:
                """
                if our SingletonServer class receives an 'A', it will know that it is a signal from our SingletonClient
                and it will respond with a 'B'. Thus, both side will know they've found each other. 
                """
                udp_client.sendto(bytes("A", encoding='utf-8'), udp_client_address)
                # Server's ip address is stored in index 0 of the tuple 'server_addr'
                recv_data_from_server, server_addr = udp_client.recvfrom(self.UDP_RECEIVE_PORT)
                msg = recv_data_from_server.decode('utf-8')

                if msg == "B":
                    server_ip_addr = server_addr[0]
                    self.connection.ip = server_ip_addr
                    recv_port_from_server, server_addr = udp_client.recvfrom(self.UDP_RECEIVE_PORT)

                    port_from_server = recv_port_from_server.decode('utf-8')
                    self.connection.port = int(port_from_server)
                    print("the port from server is: " + str(self.connection.port))
                    udp_connected = True

            except socket.timeout:
                print(" UDP Server not listening")
                udp_connected = False


    #  This function establishes a tcp connection with the server
    def connect_tcp(self):

        tcp_connected = False  
        while (tcp_connected == False):
            try:  # program tries to connect to server
                client = socket.socket()  
                address = (self.connection.ip, self.connection.port)  
                client.connect(address)  # connecting to the server 
                tcp_connected = True

            except ConnectionRefusedError:  # This exception is raised if the server is not listening
                tcp_connected = False # since there is no server, we change the boolean back to false
                print("(refused) Server not listening...")
                print(self.connection.port)
                sleep(1)

                # Client objects are one-time-use in python. Thus, we create a new one
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            except ConnectionResetError:  # raised when there is no server
                tcp_connected = False  
                print("(reset) Server not listening...")
                sleep(1)
                # Client objects are one-time-use in python. Thus, we create a new one
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.connection.client_socket_object = client
        

        # Setting a time out so if client  doesn't receive anything for 0.5 seconds, it starts sending items from priority queue
        self.connection.client_socket_object.settimeout(0.5)

        return client  # returning client, which is a socket object (TODO: is this really necessary?)


    def connect_to_server(self): # creates a client and connects it to the server
        self.connect_udp()
        self.connect_tcp()


    # "sends" data to the server
    def send(self, msg):
        self.sending_queue.put(msg + "\n")  # adding the message to the class sending  queue


    # this is the main thread of the client class which is pointed to in the initializer
    def main_thread(self):  
        self.connect_to_server()
        while True:
            try:
                msg = (self.connection.client_socket_object.recv(self.MSG_RECEIVE_PORT)).decode("utf-8")
                msg = msg.split("\n")

                for item in msg:
                    item.strip("\n")

                for item in msg:
                    print(item)  # TODO: this print statement must be changed to a function call to merge with the shell
                    # TODO: (only for UVic Robotics use)

            except socket.timeout:  # catching the timeout error
                print("timeout error while waiting to receive from server")

            except socket.error as error:
                if error == errno.ECONNRESET:  # raised if server disconnects
                    print("Server disconnected while trying to receive data from server")
                    sleep(1)
                    self.connect_to_server()

            for counter in range(10):  # sending 10 messages to the station
                if self.sending_queue.empty():
                    break
                else:
                    # we temporarily store the msg which is about to be sent so it's not lost if sending fails
                    current_msg_to_send = self.sending_queue.get()

                    try:
                        self.connection.client_socket_object.send(bytes(current_msg_to_send, encoding='utf-8'))
                        
                    except socket.error: 
                        self.sending_queue.put(current_msg_to_send)
                        print("Server disconnected while trying to send data to server")
                        sleep(1)
                        self.connect_to_server()



# The main function is only written to test the class. It is not necessary to have it.
def main():
    gate1 = Rover_Communication_Gate()
    gate2 = Rover_Communication_Gate()
    gate3 = Rover_Communication_Gate()
    gate4 = Rover_Communication_Gate()
    gate5 = Rover_Communication_Gate()


    for i in range(10000):
        gate1.send(str(i))
        sleep(1)


if __name__ == '__main__':
    main()