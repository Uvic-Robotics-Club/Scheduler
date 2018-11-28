import socket
from time import sleep

def main():
    # Setting up the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creating server object
    ip = socket.gethostbyname(socket.gethostname())  # Getting ip address of the computer
    port = 9999  # setting port to 9999
    address = (ip, port)  # creating address tuple
    server.bind(address)
    server.listen(1)

    print("Server started listening:", ip, ":", port)
    client, clientAdress = server.accept()
    #print(client)
    #print(clientAdress)
    print("Got a connection from", clientAdress[0], ":", clientAdress[1])

    while (True):
        try:
            data = client.recv(1024)
            print("[Client]:", data)

            if (data == bytes("Hello server", encoding= 'utf-8')):
                sleep(1)
                client.send(bytes("Hello to client", encoding= 'utf-8'))
            elif(data == bytes("disconnect", encoding= 'utf-8')):
                sleep(1)
                client.send(bytes("GoodBye", encoding= 'utf-8'))
                client.close()
                break
            else:
                sleep(1)
                client.send(bytes("Invalid data", encoding= 'utf-8'))

        except socket.error:
            print("Client disconnected")
            print("Waiting for client to reconnect...")
            client, clientAdress = server.accept()
            print("Client successfully reconnected")


        # The commented code below send user inputs to the client
        """ 
        Input = input(" -- ")
        Input = bytes(Input, encoding= 'utf-8')
        client.send(Input)
        """

if __name__ == '__main__':
    main()