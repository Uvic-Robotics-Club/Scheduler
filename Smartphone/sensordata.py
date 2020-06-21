class sensordata:
    def __init__ (self, name,xval,yval,zval,value_dict,sensor_dict):
        self.name = name
        self.xval = xval
        self.yval = yval
        self.zval = zval
        self.value_dict = value_dict
        self.sensor_dict = sensor_dict

    def getsensorname(self):
        return self.name
    
    def getxval(self):
        return self.xval

    def getyval(self):
        return self.yval

    def getzval(self):
        return self.zval

    def setsensorname(self,name):
        self.name = name

    def setvaluesdict(self):
        self.value_dict["x"] = self.xval
        self.value_dict["y"] = self.yval
        self.value_dict["z"] = self.zval
    
    def getvaluesdict(self):
        return value_dict

    def setsensordict(self):
        self.sensor_dict[self.name] = self.value_dict

    def getsensordict(self):
        return sensor_dict

    
    def printvalues(self):
        # print("x" < "y")
        print("These are my values: ", self.xval, self.yval,self.zval)
    
    def printvaluesdict(self):
        print(self.value_dict)

    def printsensordict(self):
        print(self.sensor_dict)

    