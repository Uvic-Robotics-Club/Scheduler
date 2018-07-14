#A simple data type containing x, y, and z values
#Also has a handy print method!
class Vector3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x = {}\ny = {}\nz = {}\n\n".format(self.x,self.y,self.z)
