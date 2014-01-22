import wx
import GUI.settings as settings
import os

STEP = 0.012
BITMAP_DIR = settings.PATH + 'generation_buffer/'

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
def drange_inclusive(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
    yield stop

def normalize(num, step=.01234):
    factor = round(num/step)
    num = step*factor
    return num

def normalize_list(iterable, step=.0001):
    l = []
    for element in iterable:
        l.append(normalize(element, step))
    return l

def fequal(a, b, error=.0001):
    """ Accounts for innacuracy in float storage.
        Given two floats it determines if they are within
        the acceptable error to be considered equal """
    diff = abs(a-b)
    return True if diff < error else False

def Point3D(x,y,z):
    return (x,y,z)

class LineSegment():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
    def get_slope(self):
        numerator = self.y2 - self.y1
        denom = self.x2 - self.x1
        if fequal(denom, 0):
            return float('inf')
        else:
            return numerator/denom

    def calc_x(self, y):
        """ Given a y value, it returns the points at the intersections of self and the line y=y"""
        y = float(y)
        m = self.get_slope()
        if y<=max(self.y1, self.y2) and y>=min(self.y2, self.y1):
            if m == float('inf'):
                #If vertical, and y is in range, we want the point that satisfies the x of the line and the given y
                return [(self.x1, y)]
            if m == 0:
                #If horizontal, to satisfy initial condition we know it is already equal, so return both endpoints
                if fequal(self.x1, self.x2):
                    #If both points are the same, just return one
                    return [(self.x1, y)]
                return [(self.x1, y), (self.x2, y)]
            #For normal points on a non-vertical, and non-horizontal line, simply use point slope calculation
            x = ((y-self.y1)/m)+self.x1
            return [(x,y)]
        else:
            return [] #No intersection

    def calc_y(self, x):
        """ Given a x value, it returns the points at the intersections of self and the line x=x"""
        x = float(x)
        m = self.get_slope()
        if x<=max(self.x1, self.x2) and x>=min(self.x1, self.x2):
            if fequal(m, 0.0):
                #If line is horizontal, and x is in domain, we want only the point at x with the y of the line
                return [(x, self.y1)]
            if m == float('inf'):
                #The line is vertical, and x has already been confirmed to be in domain, so is equal to x of line
                if fequal(self.y1, self.y2):
                    #If marked as vertical because it is defined by two of the same points, return just one copy of the point
                    return [(self.x1, self.y1)]
                else:
                    #REturn the endpoints, because on this non-function segment their are two acceptable y-values
                    return [(self.x1,self.y1), (self.x2,self.y2)]
            #For normal points on a non-vertical, and non-horizontal line, simply use point slope calculation
            y = (m*(x-self.x1))+self.y1
            return [(x,y)]
        else:
            return [] #There is no intersection

class Line3d():
    def __init__(self, p1, p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.z1 = p1[2]
        self.x2 = p2[0]
        self.y2 = p2[1]
        self.z2 = p2[2]

    def calc_xy(self, z):
        z = float(z)
        line_xz = LineSegment(self.x1, self.z1, self.x2, self.z2) #Define line with X as independent, Z as dependent
        x_list = line_xz.calc_x(z)                                #Calculate the specific X for the given Z
        if len(x_list)<1:
            #does not cross this z value
            return []
        else:
            points = []
            x = x_list[0][0]
            line_xy = LineSegment(self.x1, self.y1, self.x2, self.y2)
            y = line_xy.calc_y(x)
            if len(y)<1:
                #Is not part of the domain
                return None
            points.append((x, y[0][1]))
            if len(y)>1:
                points.append((x, y[1][1]))

            if len(x_list)>1:
                x = x_list[1][0]
                y = line_xy.calc_y(x)
                if len(y)<0:
                    #Is not part of the domain
                    return None
                points.append((x, y[0][1]))
                if len(y)>1:
                    points.append((x, y[1][1]))
            return points

class Facet:
    def __init__(self, p1, p2, p3, normal=(0.0,0.0,0.0)):
        self.a = Line3d(p1, p2)
        self.b = Line3d(p2, p3)
        self.c = Line3d(p3, p1)
        self.normal = normal
    def print_lines(self):
        for line in (self.a, self.b, self.c):
            """print (line.x1, line.y1, line.z1)
            print (line.x2, line.y2, line.z2)
            print"""
            pass
    def max_z(self):
        return max(self.a.z1, self.a.z2,
                self.b.z1, self.b.z2,
                self.c.z1, self.c.z2)
    def min_z(self):
        return min(self.a.z1, self.a.z2,
                self.b.z1, self.b.z2,
                self.c.z1, self.c.z2)
    def add_to_bmps(self, dir = None, filename=None):
        z1 = normalize(self.min_z(), STEP)
        z2 = normalize(self.max_z(), STEP)
        name = filename.replace('.stl', '')
        for z in drange_inclusive(z1, z2, STEP):
            full_name = get_zlevel_full_name(z, dir, name)
            bmp = get_zlevel_bmp(full_name)
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.SetBrush(wx.Brush(wx.Colour(0,0,255)))
            for line in (self.a, self.b, self.c):
                for point in line.calc_xy(z):
                    PPI = 400
                    dc.DrawRectangle(0,0, point[0]*PPI, point[1]*PPI)
            dc.SelectObject(wx.NullBitmap)
            bmp.SaveFile(full_name, wx.BITMAP_TYPE_BMP)

#read text stl match keywords to grab the points to build the model
def process_file(filename):
    f = open(filename,'r')
    basic_name = filename[filename.rfind('/'):]
    print 'after cut' + basic_name
    facets = []
    triplet = []
    for line in f.readlines():
        words = line.split()
        if len(words) > 0:
            if words[0] =='vertex':
                #Get the points of the vertex:
                #Normalize the Z component to a valid step layer, so we don't miss horizontal lines or facets
                point = (eval(words[1]), eval(words[2]), normalize(eval(words[3]), STEP))
                triplet.append(point)
                if len(triplet) >= 3:
                    p1,p2,p3 = triplet
                    facets.append(Facet(p1,p2,p3))
                    triplet = []
    for facet in facets:
        facet.add_to_bmps(BITMAP_DIR, basic_name)
    print "done"
    f.close()

def get_zlevel_bmp(full_name):
    """Returns wxBitmap for the given z-layer
            -If a bitmap exists, it uses it as a base
            -otherwise it creates an empty bitmap at that layer"""
    if not os.path.isfile(full_name):
        #if it doesn't exist, make a new bitmap
        x, y = settings.BUILD_PIXELS
        bitmap = wx.EmptyBitmap(x, y, -1)
        print 'tried to save'+full_name
        bitmap.SaveFile( full_name, wx.BITMAP_TYPE_BMP )
    zbmp = wx.Bitmap(full_name)
    #zbmp.LoadFile(full_name)
    return zbmp

def get_zlevel_full_name(z, path, name):
    """Creates a unique bitmap name for each layer"""
    #We use the z value and the name of the original file to generate a name
    level_num = str(z)
    decimal = len(level_num)- min(0, level_num.find('.')) #Record the places beyond the decimal, so 12 and .12 don't save to same layer
    decimal = str(decimal)
    level_num.replace('.','')#remove decimal point
    prefix = path + name
    suffix = '.bmp'
    full_name = prefix + decimal + '-' + level_num + suffix
    return full_name


def main():
    app = wx.App()
    """l = [12.34, 123.485602648, 1, 3.4, -7.6, -4]
    print l
    print normalize_list(l, .0002345)
    a=3.20000347
    b=3.200005
    print 'Are theses equal?',a,' ',b
    print fequal(a, b)"""
    p1 = Point3D(0,0,1)
    p2 = Point3D(0,0,0)
    p3 = Point3D(1,1,1)
    face = Facet(p1, p2, p3)
    #face.add_to_bmps()
    #l_3D = Line3d(p2, p1)
    process_file(settings.PATH+'examples/temp_file.stl')
    heyy = False
    while heyy:
        z = input("Give Z, I'll find its XY intercepts.")
        if z != 'n':
            print"For z = ", z, " the points on a plane parallel to the XY plane are:"
            print l_3D.calc_xy(z), '\n'
        else:
            heyy = False
    app.Destroy()

if __name__ == '__main__':
    main()