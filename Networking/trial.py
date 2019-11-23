import json






def main():
    A = [[1,2,3], [4,5,6], 7,8,9]

    new = json.dumps(A)

    print(type(A))
    print(type(new))
    print(type(json.loads(new)))








if __name__ == '__main__':
    main()