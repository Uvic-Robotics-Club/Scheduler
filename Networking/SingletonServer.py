import socket
from time import sleep
import queue
from threading import Thread
import errno  # this is used for handling specific errors for the socket module
# TODO: increment port for UDP in case it is occupied already
# todo: be aware that messages that are failed to be sent due to a failure, are added to the end of the queue, so it
#  takes them a while to reach the client
# todo: there are 'sleep' commands in this program; these are there to enable the user to see the output of
#   the programme and make sure of the correct functionality. However, while using the class for actual purposes, these
#   should be commented out.
# todo: The main function is only written to test the class. It is not necessary to have it.

class Connection:
    def __init__(self, server_socket_object=None, server_ip=None, port=None, client_socket_object=None, client_address=None):
        self.server_socket_object = server_socket_object
        self.server_ip = server_ip
        self.port = port
        self.client_socket_object = client_socket_object
        self.client_address = client_address


class Station_Communication_Gate():

    # the 'connection' variable is shared among all instances of this class. Thus, it could be use to give this class a
    # ~ singleton behaviour
    connection = None

    sending_queue = queue.Queue()  # a queue that contains all data that needs to be sent to the rover
    # ~ since a queue is a complex object, it is shared among all objects of the class

    INITIAL_PORT = 6663
    UDP_BROADCAST_PORT = 9999
    UDP_RECEIVE_PORT = 2048
    MSG_RECEIVE_PORT = 1024
    MAXIMUM_PORT_NUMBER = 65533

    # the server can figure out its own ip and port is hardcoded. Hence, no parameter is need for the initializer.
    def __init__(self):
        if (self.connection == None):  # checks if server is listening
            print("Creating an object")
            """
            EXTREMELY IMPORTANT: 
            Note the syntax below. Writing 'Station_Communication_Gate.connection' instead of 'self.connection'
            results in singleton behaviour. 
            DO NOT CHANGE THE SYNTAX!
            """
            Station_Communication_Gate.connection = Connection(port=self.INITIAL_PORT)

            t = Thread(target=self.main_thread)  # connection is established in the thread
            t.start()

        else:
            # An instance of this class has been previously created; nothing happens
            pass

    # used to increment a port in case it is occupied already
    def increment_port(self):
        self.connection.port = (self.connection.port + 1) % self.MAXIMUM_PORT_NUMBER

        ignored_ports = [1024, 2048, 9999]  # these are dicey port; better to be avoided
        if (self.connection.port in ignored_ports):
            self.connection.port = (self.connection.port + 1) % self.MAXIMUM_PORT_NUMBER

        print("the port incremented to: " + str(self.connection.port))

    def connect_udp(self):
        udp_address = (socket.gethostbyname(""), self.UDP_BROADCAST_PORT) # the address that the udp server will bind to
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating a UDP server to listen to broadcasts
        # ~ by the UDP client

        udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # setting udp protocols for the object
        udp_server.bind(udp_address)

        udp_client_connected = False
        while udp_client_connected == False:
            print("UDP server listening")
            # recv_data would be the data sent by the client to the server. udp_client_address would be address of the client
            recv_data, udp_client_address = udp_server.recvfrom(self.UDP_RECEIVE_PORT)
            msg = recv_data.decode("utf-8")  # decoding the received message from client

            if (msg == "A"):
                print("the correct UDP client connected")
                udp_server.sendto(bytes("B", encoding='utf-8'), udp_client_address)
                udp_server.sendto(bytes(str(self.connection.port), encoding='utf-8'), udp_client_address)
                udp_client_connected = True

            else:
                udp_server.sendto(bytes("Connection denied!", encoding='utf-8') + recv_data, udp_client_address)

        udp_server.close()  # closing the server

    def connect(self):
        """
        First, we create a UDP server which can listen to the UDP client. After the UDP client and server are connected
        then we will establish a TCP connection between the two devices.

        """
        self.connection.server_socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.server_ip = socket.gethostbyname("")

        while True:
            try:
                # binding the server to the address (ip, port)
                self.connection.server_socket_object.bind((self.connection.server_ip, self.connection.port))
                break
            except socket.error:  # raised when address is already in use (port occupied)
                self.increment_port()

        self.connect_udp()

        self.connection.server_socket_object.listen(1)

        print("Server started listening:", self.connection.server_ip, ":", self.connection.port)

        client, tcp_client_address = self.connection.server_socket_object.accept()
        print("Client successfully connected")
        self.connection.client_socket_object = client
        self.connection.client_address = tcp_client_address

        # Setting a time out so if the server doesn't receive anything for 0.5 seconds, it starts sending items from priority queue
        self.connection.client_socket_object.settimeout(0.5)


    # "sends" data to the client
    def send(self, msg):
        self.sending_queue.put(msg + "\n")


    # this is the main thread of the server which is pointed to in the initializer
    def main_thread(self):
        self.connect()
        while True:
            try:
                msg = self.connection.client_socket_object.recv(self.MSG_RECEIVE_PORT).decode("utf-8")
                msg = msg.split("\n")
                for item in msg:
                    item.strip("\n")

                for item in msg:
                    print(item)  # todo: this print statement must be changed to a function call to merge with the shell
                    # todo: (only for UVic Robotics use)

            except socket.timeout:  # catching the timout error
                print("time out error while waiting to receive from client")

            except socket.error as error:
                if error == errno.ECONNRESET:  # raised if client disconnects
                    print("Client disconnected while trying to receive data from client")
                    print("Waiting for client to reconnect...")

                    self.connection.server_socket_object.close()
                    # getting connection from (new) client again
                    self.connect()

            for counter in range(10):  # sending 10 messages to the rover
                if self.sending_queue.empty():
                    break
                else:
                    # we temporarily store the msg which is about to be sent so it's not lost if sending fails
                    current_msg_to_send = self.sending_queue.get()

                    try:
                        self.connection.client_socket_object.send(bytes(current_msg_to_send, encoding='utf-8'))

                    except socket.error:
                        self.sending_queue.put(current_msg_to_send)
                        print("Client disconnected while trying to send data to client")
                        print("Waiting for client to reconnect...")

                        self.connection.server_socket_object.close()
                        self.connect()
                    else:
                        pass


# The main function is only written to test the class. It is not necessary to have it.
def main():
    gate = Station_Communication_Gate()
    gateS2 = Station_Communication_Gate()


    for i in range(10000):
        gate.send(str(i))
        sleep(1)


if __name__ == '__main__':
    main()
