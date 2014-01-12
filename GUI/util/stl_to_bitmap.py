def normalize(num, step=.01234):
    factor = round(num/step)
    num = step*factor
    return num

def normalize_list(iterable, step=.01234):
    l = []
    for element in iterable:
        l.append(normalize(element, step))
    return l

def fequal(a, b, error=.00001):
    """ Accounts for innacuracy in float storage.
        Given two floats it determines if they are within
        the acceptable error to be considered equal """
    diff = abs(a-b)
    return True if diff < error else False


class Line3d():
    def __init__(self, p1, p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.z1 = p1[2]
        self.x2 = p2[0]
        self.y2 = p2[1]
        self.z2 = p2[2]
        
    def get_xy(self, z):
        line_xz = Line2D(self.x1, self.z1, self.x2, self.z2) #Define line with X as independent, Z as dependent
        x = line_xz.calc_x(z)                                #Calculate the specific X for the given Z
        line_xy = Line2D(self.x1, self.y1, self.x2, self.y2)
        y = line_xy.calc_y(x)
        return (x,y)



class Line2D():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
    def get_slope(self):
        numerator = self.y2 - self.y1
        denom = self.x2 - self.x1
        return numerator/denom
    def calc_x(self, y):
        """ Given a y value, it returns the x value """
        m = self.get_slope()
        x = ((y-self.y1)/m)+self.x1
        return x
    def calc_y(self, x):
        """ Given a x value, it returns the y value """
        m = self.get_slope()
        y = (m*(x-self.x1))+self.y1
        return y

class Point3D():
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def get_x(self):
        return self.x
    def set_x(self, num):
        self.x=num
    x = property(self.get_x, self.set_x)
    def get_y(self):
        return self.y
    def set_y(self, num):
        self.y=num
    y = property(self.get_y, self.set_y)
    def get_z(self):
        return self.z
    def set_z(self, num):
        self.z=num
    z = property(self.get_z, self.set_z)


def main():
    l = [12.34, 123.485602648, 1, 3.4, -7.6, -4]
    print l
    print normalize_list(l, .0002345)
    a=3.20000347
    b=3.200005
    print 'Are theses equal?',a,' ',b
    print fequal(a, b)

if __name__ == '__main__':
    main()