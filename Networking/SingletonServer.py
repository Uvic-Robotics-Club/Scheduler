import socket
from time import sleep
import queue
from threading import Thread
import errno  # this is used for handling specific errors for the socket module

# todo: be aware that messages that are failed to be sent due to a failure, are added to the end of the queue, so it
#  takes them a while to reach the client
# todo: there are 'sleep' commands in this program; these are there to enable the user to see the output of
#   the programme and make sure of the correct functionality. However, while using the class for actual purposes, these
#   should be commented out.
# todo: The main function is only written to test the class. It is not necessary to have it.


class Station_Communication_Gate():
    classConnectionList = [None, None, None, None, None]
    #  classConnectionList --> [server socket Object , ip (of server itself), port , client connected to the server ,
    # ... address of client connected to the server ]

    sending_queue = queue.Queue()  # a queue that contains all data that needs to be sent to the rover
    # since a queue is a complex object, it is shared among all objects of the class

    # the server can figure out its own ip and port is hardcoded. Hence, no parameter is need for the initializer.
    def __init__(self):
        if (self.classConnectionList == [None, None, None, None, None]):  # checks if server is listening
            self.classConnectionList[2] = 6663  # storing the port in index 2

            # connection is established in the thread
            self.connect()
            t = Thread(target=self.main_thread)  # setting the main thread
            t.start()  # starting the main thread

        else:  # this else statement runs if an instance of the class exists already
            pass

    def connect(self):
        """
        First, we create a UDP server which can listen to the UDP client. After the UDP client and server are connected
        then we will establish a TCP connection between the two devices.

        """
        self.classConnectionList[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a server socket
        # ... and storing it in index 0 of classConnectionList
        self.classConnectionList[1] = socket.gethostbyname("")  # storing ip in index 1

        """
        Due to the use of threads in this programme, sometimes when a process is killed (in this case only the server)
        the socket does not close, and hence the address that the server has bind to, will still be in use. Thus, when 
        the program is rerun, and the server tries to bind to the address, the ' address already in use' error wil 
        occur. to take care of this, we have the below try and catch clauses so that id an address is already in use, 
        the port number would be incremented by 1, and then both port number and the ip address of the server would be 
        sent to the UDP client using a UDP server and the a TCP connection would be established between the two sides.
        """
        while True:
            try:
                self.classConnectionList[0].bind((self.classConnectionList[1], self.classConnectionList[2]))  # binding
                # ~ the server to the address(ip, port)
                break
            except socket.error:
                self.classConnectionList[2] = (self.classConnectionList[2] + 1) % 65533
                print()
                if (self.classConnectionList[2] == 1024):  # dicey port; better to be avoided
                    self.classConnectionList[2] = (self.classConnectionList[2] + 1) % 65533
                if (self.classConnectionList[2] == 2048):  # dicey port; better to be avoided
                    self.classConnectionList[2] = (self.classConnectionList[2] + 1) % 65533
                if (self.classConnectionList[2] == 9999):  # dicey port; better to be avoided
                    self.classConnectionList[2] = (self.classConnectionList[2] + 1) % 65533
                print("the port incremented to: " + str(self.classConnectionList[2]))

        UDP_address = (socket.gethostbyname(""), 9999)  # the address that the udp server will bind to
        UDP_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating a UDP server to listen to broadcasts
        # ~ by the UDP client
        UDP_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # this function is called to so this tserver
        # ~ used UDP protocol
        UDP_server.bind(UDP_address)  # binding the UDP server to the address

        UDP_client_connected = False
        while UDP_client_connected == False:
            print("UDP server listening")
            recv_data, UDP_client_adr = UDP_server.recvfrom(2048)  # recv_data would be the data sent by the client
            # ~ to the server. UDP_client_adr would be address of the client
            msg = recv_data.decode("utf-8")  # decoding the received message from client

            if (msg == "A"):
                print("the correct UDP client connected")
                UDP_server.sendto(bytes("B", encoding='utf-8'), UDP_client_adr)
                UDP_server.sendto(bytes(str(self.classConnectionList[2]), encoding='utf-8'), UDP_client_adr)
                UDP_client_connected = True

            else:
                UDP_server.sendto(bytes("Connection denied!", encoding='utf-8') + recv_data, UDP_client_adr)

        UDP_server.close()  #closing the server

        self.classConnectionList[0].listen(1)  # server starts listening

        UDP_server.close()  # closing the server

        print("Server started listening:", self.classConnectionList[1], ":", self.classConnectionList[2])

        client, clientAddress = self.classConnectionList[0].accept()
        print("Client successfully connected")
        self.classConnectionList[3] = client  # storing the new client in index 3 of classConnectionList
        self.classConnectionList[4] = clientAddress  # storing the address of the new client in index 4 of
        self.classConnectionList[3].settimeout(0.5)  # setting a time out for the thread so it doesn't spend time on the
        # ... task for more than two seconds; so if it doesn't receive anything for 0.5 seconds, it stops trying to
        # ... receive sth from client and starts sending stuff, if there are any

    def send(self, msg):  # it is used to send data to client
        self.sending_queue.put(msg + "\n")  # adds the msg to the sending_queue

    def main_thread(self):  # this is the main thread of the server which is pointed to in the initializer

        while True:  # all thread functions must have a while loop inside them
            try:  # trying to receive a message from client
                msg = self.classConnectionList[3].recv(1024).decode("utf-8")  # since tye string was encoded to bytes
                # ... for sending by the client, it has to be decoded now
                msg = msg.split("\n")
                for item in msg:
                    item.strip("\n")

            except socket.timeout:  # catching the timout error
                print("time out error while waiting to receive from client")

            except socket.error as error:
                if error == errno.ECONNRESET:  # checking if the raised error is "ECONNRESET" type
                    # "ECONNRESET" is the exception that is raised when the other end is disconnected. In this case,
                    # ... this error is raised if client disconnects
                    print("Client disconnected while trying to receive data from client")
                    print("Waiting for client to reconnect...")

                    self.classConnectionList[0].close()
                    # getting connection from (new) client again
                    self.connect()
            else:  # runs only if no exception has been raised
                for item in msg:
                    print(item)  # todo: this print statement must be changed to a function call to merge with the shell
                    # todo: (only for UVic Robotics use)

            for counter in range(10):  # the for loop is intended to send 10 messages to the rover
                if self.sending_queue.empty():  # checking if the sending_queue is not empty
                    break
                else:
                    try:  # trying to send sth from the sending queue to the client
                        currentMsgToSend = self.sending_queue.get()  # storing the msg that is about to be sent so if
                        # ... the server fails to send it, it gets added to the queue and is not lost
                        self.classConnectionList[3].send(bytes(currentMsgToSend, encoding='utf-8'))
                        #print("DATA WAS SENT TO CLIENT")

                    except socket.error:  # this is a general socket error which also covers "connection reset by peer"
                        self.sending_queue.put(currentMsgToSend)
                        print("Client disconnected while trying to send data to client")
                        print("Waiting for client to reconnect...")

                        self.classConnectionList[0].close()
                        # getting connection from (new) client again
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
