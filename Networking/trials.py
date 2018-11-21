def main():
    list = ["Zhan", "Shayan", "Amir"]
    del list[0]
    del list[0]
    del list[0]
    print(list)

    userInput = float(input("Type a float"))
    if (0 < userInput < 1):
        print("YAAAAY")



if __name__ == '__main__':
    main()