#Scott Krulcik 10/29

def tri(data):
    return trap(data)#testing only

def trap(data):
    line1=[(1,2),(2,4),(3,9),(4,16),(5,25)]
    line2=[(-4,3),(-3,3),(-2,2),(-1,2),(0,3)]
    line3=[(1,3),(2,2),(3,2),(4,3),(5,3)]
    return (line1, line2, line3)#testing only


shapes={"triangle":tri, "trapezoid":trap}

class Gear():
    def __init__(self, diameter, teeth, bore=None, shape="triangle"):
        self.d=diameter
        self.numTeeth=teeth
        self.bore=bore
        self.shape=shape

    def getDescription(self):
        return "gear template"

    def getData(self):
        global shapes
        if(shapes.has_key(self.shape)):
            self.shape="triangle"
        return shapes[self.shape]([2,3])

    def getDiameter(self):
        return self.d
    def setDiameter(self, value):
        self.d = value
    diameter = property(getDiameter, setDiameter, doc="Pitch diameter")

    def getBore(self):
        return self.bore
    def setBore(self, value):
        self.bore = value
    boreDiameter = property(getBore, setBore, doc="Bore diameter")

    def getTeeth(self):
        return self.numTeeth
    def setTeeth(self, value):
        self.numTeeth = value
    numberOfTeeth = property(getTeeth, setTeeth, doc="Number of teeth around the gear")