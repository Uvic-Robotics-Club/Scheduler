import json

class JoyPackeger():
    def __init__(self):
        pass

    def package(self, array):

        array.append("JoyData")
        return json.dumps(array)




















