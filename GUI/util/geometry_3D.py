from app_util import fequal

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
                return []
            points.append((x, y[0][1]))
            if len(y)>1:
                points.append((x, y[1][1]))

            if len(x_list)>1:
                x = x_list[1][0]
                y = line_xy.calc_y(x)
                if len(y)<1:
                    #Is not part of the domain
                    return []
                points.append((x, y[0][1]))
                if len(y)>1:
                    points.append((x, y[1][1]))
            return points