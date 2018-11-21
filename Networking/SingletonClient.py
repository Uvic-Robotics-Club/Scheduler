# comment the code
# documentation regarding how to use the code
# Add a "send" function
# get rid of while loop
# All errors handled inside the class itself
# add threading
# make restart connection method work

class Communication_Gate:
    class_connection_list = []
    """
    ---     USING A CLASS VARIABLE TO CREATE THE EFFECTS OF A SINGLETON CLASS ---
    having a "connection" or "client socket object" as class variable which is SHARED among all objects and is reset 
    after a new instance of the class is created, would be operating just like a singleton class.
    There are two types of objects in python: simple and complex. when a simple object is reused, it is copied to a
    new memory location and used, and this is done because the object is simple and it is easy to copy the object. Such
    objects are strings, integers, and booleans. 
    When a complex object is reused, the programmer just uses a pointer to point to the same memory location.
    Hence, any changes made to that memory location, would affect all other objects that are using that pointer.
    As a result, if we use a complex object like a list as a class variable, its going to be declared only once and 
    would result in a singleton behaviour for this class.
    """
    def __init__(self, ip, port):
        if  (self.class_connection_list == []):  # check if no connection exists

            self.class_connection_list.append(self.connectToServer(ip, port)) #creating a socket client object and
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

    def connectToServer(self, ip, port): # Creates a client and connects it to the server
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

        return client #returning client, which is a socket object
    def restartConnection(self):
        self.class_connection_list = []
        print("HIHI")


def main():
    port = 9999  # setting port to 9999
    # Setting up client
    ipOfServer = socket.gethostbyname(socket.gethostname())  # getting ip address of the server (this computer for now!)
    gate = Communication_Gate(ipOfServer, port)
    gate2 = Communication_Gate("HEEEEYY", 2000000)
    gate3 = Communication_Gate("BITCH", 900001)

    while (True):
        list_cleaned = False  # this indicates if the 'class_connection_list' is not emptied
        try:
            gate.class_connection_list[0].send(bytes("Hello server", encoding='utf-8'))
            gate2.class_connection_list[0].send(bytes("Gate2 is working", encoding='utf-8'))
            gate3.class_connection_list[0].send(bytes("Even 3 is working", encoding='utf-8'))
            Data = gate.class_connection_list[0].recv(1024)

            print("Server said", Data)
        except socket.error:  # If connection is lost (server stops listening), client waits for server to start
            # ... listening again and then connects to it again
            """
            Notice the connection of the initial client object has failed. If we try to create a new object, it will 
            point to the previous object as it is supposed to. However, the previous object is broken and is not 
            working. Hence, we need to completely empty the 'class_connection_list' se when we try to create a new 
            object, the program actually creates a new object.
            """
            sleep(1)
            if (list_cleaned == False):
                for counter in range(3):
                    del gate.class_connection_list[0]
                list_cleaned = True  # setting the value to true since the 'class_connection_list' is now emptied
            gate = Communication_Gate(ipOfServer, port)  # creating a new object. And this actually creates a new object
            # ... since the 'class_connection_list' list is empty now which further objects will point to it

if __name__ == '__main__':
    main()
    if error:
        comms = Communication_Gate()
        sent = comms.send(data)
    #handle error