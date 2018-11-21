import socket
from time import sleep

# take care of sending multiple messages without receiving one


def connectToServer(ip, port): # Creates a client and connects it to the server
    # "ip" is the ip of the server that this client is trying to connect to

    connectedToServer = False  # Defining a boolean to show whether client is connected to server
    while (connectedToServer == False):  # trying to connecting the client to the server while it is not connected
        try:  # program tries to connect to server
            client = socket.socket()  # creating client object
            address = (ip, port)  # creating address tuple
            client.connect(address)  # connecting to the server using address
            connectedToServer = True  # assuming that the client has successfully has connected to the server and hence,
            # ...changing the boolean accordingly (if connecting fails, the exception clause below will run
        except ConnectionRefusedError: # This exception is raised if the server is not listening
            connectedToServer = False # since there is no server, we change the boolean back to false
            print("Server not listening...")
            sleep(1)
            client = socket.socket()  # since there has been a failed connection for the previous client object,
            #...something has changed inside it and hence, it can not try to connect agin. So we create a new client object.

    return client #returning client, which is a socket objects


def main():
    port = 9999 # setting port to 9999
    # Setting up client
    ipOfServer = socket.gethostbyname(socket.gethostname()) #getting ip address of the server (this computer for now!)
    client = connectToServer(ipOfServer, port)

    while(True):
        try:
            client.send(bytes("Hello server", encoding= 'utf-8'))
            Data = client.recv(1024)
            print("Server said", Data)
        except socket.error: #If connection is lost (server stops listening), client waits for server to start
                             #... listening again and then connects to it again
            client = connectToServer(ipOfServer, port)



if __name__ == '__main__':
    main()
