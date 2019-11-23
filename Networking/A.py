from SingletonClient import Rover_Communication_Gate
from JoyPackeger import JoyPackeger

def main():
    client = Rover_Communication_Gate()

    Array = [2, 3]

    packeger = JoyPackeger()

    client.send(packeger.package(Array))
















if __name__ == '__main__':
    main()