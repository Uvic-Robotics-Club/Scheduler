
class yee:
    def __init__(self, a=None, h=None):
        self.a = a
        self.h = h

class human:

    yup = None

    def __init__(self, age=None, height=None):
        if (self.yup == None):
            print("creating an object")
            human.yup = yee(age, height)
            print(self.yup)
        else:
            pass



def main():
    shayan = human(10)
    y = human(90, 100)

    z = human(30, 40)

    print(shayan.yup.a)
    print(y.yup.a)
    print(z.yup.a)

if __name__ == '__main__':
    main()