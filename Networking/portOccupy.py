import socket
from time import sleep
from threading import Thread
import socket
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a TCP socket
    port = 6664
    ip = socket.gethostbyname("")


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