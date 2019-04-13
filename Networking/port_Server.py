import socket



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket
    port = 6663
    ip = socket.gethostbyname("")

    """
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket
    server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket
    server4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket
    server5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket

    server2.bind((ip, 5001))
    server3.bind((ip, 5002))
    server4.bind((ip, 5003))
    server5.bind((ip, 5004))
    """


    while True:
        try:
            server.bind((ip, port))
            print("server started listening on port %d , ip %s" % (port, ip))
            server.listen(1)
            client, clientAddress = server.accept()
            print("hi")
            break

        except OSError:
            print("The address was already in use. Going to try a different port")
            port = (port+1) % 65534

    print(port)






















if __name__ == '__main__':
    main()