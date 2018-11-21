# This program is an example of singleton implementation
# Hence if more than one Human object is created, it will be a pointer to the very first
# ... Human object that was created

class Human:
    instance = None

    if not instance:
        instance = True


    connection_root = 10
    def __init__(self):
        self.age = 18
        self.name = "Shayan"

    def printInfo(self):
        print(self.name, "is", self.age)




def main():
    Ben = Human()
    Ben.printInfo()
    Shayan = Human()
    Shayan.printInfo()
    Zhan = Human()

    print("+++++++++++++++")
    Zhan.printInfo()
    print("Below")
    Shayan.printInfo()
    Ben.printInfo()




if __name__ == '__main__':
    main()