import socket
from time import sleep
import queue
from threading import Thread
import errno  # this is used for handling specific errors for the socket module

# try all the hosts and then connect

class Station_Communication_Gate():
    classConnectionList = []
    #  classConnectionList --> [server socket Object , ip , port , client connected to the server ,
    # ... address of client connected to the server ]

    sending_queue = queue.Queue()  # a queue that contains all data that needs to be sent to the rover
    # since a queue is a complex object, it is shared among all objects of the class

    def __init__(self, ip, port):
        if (self.classConnectionList == []):  # checks if server is listening
            self.classConnectionList.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))  # creating a server
            # ... and storing it in index 0 of classConnectionList
            self.classConnectionList.append(ip)  # storing ip in index 1
            self.classConnectionList.append(port)  # storing port in index 2
            self.classConnectionList[0].bind((ip, port))  # binding the server to the address(ip, port)
            self.classConnectionList[0].listen(1)  # server starts listening
            print("Server started listening:", ip, ":", port)

            client, clientAddress = self.classConnectionList[0].accept()
            self.classConnectionList.append(client)  # storing the client that has connected to the server in
            # ... index 3 of classConnectionList
            self.classConnectionList.append(clientAddress)  # storing the address of the client that has connected to
            # ... the server in index 5 of classConnectionList
            print("Got a connection from", clientAddress[0], ":", clientAddress[1])

            t = Thread(target= self.main_thread)  # setting the main thread
            t.start()  # starting the main thread

        else:  # this else statement runs if an instance of the class exists already
            pass

    def send(self, msg):  # it is used to send data to client
        self.sending_queue.put(msg + "\n")  # adds the msg to the sending_queue

    def main_thread(self):  # this is the main thread of the server which is pointed to in the initializer
        self.classConnectionList[3].settimeout(0.5)  # setting a time out for the thread so it doesn't spend time on the
        # ... task for more than two seconds; so if it doesn't receive anything for 0.5 seconds, it stops trying to
        # ... receive sth from client and starts sending stuff, if there are any

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

                    # getting connection from (new) client again
                    client, clientAddress = self.classConnectionList[0].accept()
                    print("Client successfully reconnected")
                    self.classConnectionList[3] = client  # storing the new client in index 3 of classConnectionList
                    self.classConnectionList[4] = clientAddress  # storing the address of the new client in index 4 of
                    self.classConnectionList[3].settimeout(0.5)  # timeout has to be reset since it is a new object
                    # ... classConnectionList
            else:  # runs only if no exception has been raised
                for item in msg:
                    print(item)

            for counter in range(10):  # the for loop is intended to send 10 messages to the rover
                if self.sending_queue.empty():  # checking if the sending_queue is not empty
                    break
                else:
                    try:  # trying to send sth from the sending queue to the client
                        currentMsgToSend = self.sending_queue.get()  # storing the msg that is about to be sent so if
                        # ... the server fails to send it, it gets added to the queue and is not lost
                        self.classConnectionList[3].send(bytes(currentMsgToSend, encoding='utf-8'))
                        print("DATA WAS SENT TO CLIENT")

                    except socket.error:  # this is a general socket error which also covers "connection reset by peer"
                        self.sending_queue.put(currentMsgToSend)
                        print("Client disconnected while trying to send data to client")
                        print("Waiting for client to reconnect...")

                        # getting connection from (new) client again
                        client, clientAddress = self.classConnectionList[0].accept()
                        print("Client successfully reconnected")
                        self.classConnectionList[3] = client  # storing the new client in index 3 of classConnectionList
                        self.classConnectionList[4] = clientAddress  # storing the address of the new client in index 4
                        # ... of the classConnectionList
                        self.classConnectionList[3].settimeout(0.5)  # timeout has to be reset since it is a new object
                        # ... classConnectionList
                    else:
                        pass


def main():
    ip = socket.gethostbyname("")  # Getting ip address of the computer
    port = 45454  # setting port to 9999
    gate = Station_Communication_Gate(ip, port)
    gateS2 = Station_Communication_Gate("QQQQQQQQ", 27477774774)
    for i in range(10000):
        gate.send(str(i))


if __name__ == '__main__':
    main()