from threading import Thread
import time

def timer(name, delay, repeat):
    print("Timer:", name, "Started")
    while repeat > 0:
        time.sleep(delay)
        print(name, ":", str(time.ctime(time.time())))
        repeat -= 1
    print("Timer", name, " completed")

def printer():
    while 1:
        time.sleep(1)
        #data = input("Enter the string: ")
        print("Your data is:")

def main():
    t1 = Thread(target=timer, args=("Timer1", 3, 5))
    t2 = Thread(target=printer)
    t1.start()
    t2.start()

    print("Main completed")






if __name__ == '__main__':
    main()