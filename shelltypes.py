#A simple data type containing x, y, and z values
#Also has a handy print method!
class Vector3:

    def __init__(self, ex=0, why=0, zed=0):
        self.x = ex
        self.y = why
        self.z = zed

    def __str__(self):
        return "x = {}\ny = {}\nz = {}\n\n".format(self.x,self.y,self.z)
