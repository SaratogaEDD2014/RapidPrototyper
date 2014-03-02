from numpy import *
from wx import *

tri1 = [(0,0),(1,0)]
tri2 = [(1,0),(0,1)]
tri3 = [(0,1),(0,0)]

rect1 = [(1,1),(1,2)]
rect2 = [(3,1),(3,2)]
rect3 = [(1,1),(3,1)]
rect4 = [(3,2),(1,2)]

app = App()
frm = Frame(None, size=(400,400))
frm.Show(True)

IN_BRUSH = wx.Brush(wx.Colour(0,0,0))
OUT_BRUSH = wx.Brush(wx.Colour(255,0,0))

class Polygon(Object):
    def __init__(self, vertices=[]):
        self.vertices = vertices
    def length(self):
        """Returns the number vertices in the polygon.
            *NOTE: Does not always match number of sides because first and last may be same point"""
        return len(self.vertices)
    def add_vertices(self, points):
        """add_vertices(self, points):
        Adds a list of points to polygon."""
        self.vertices += points
    def add_vertex(self, vertex):
        """add_vertex(self, vertex):
        Adds single point to polygon"""
        self.vertices.append(vertex)
    def set_vertices(self, vertices):
        """set_vertices(self, vertices):
            Completely replaces vertices with new ones"""
        self.vertices = vertices

class ConcentricPoly(Polygon):
    def __init__(self, vertices=[], positivity=True):
        super(ConcentricPoly, self).__init__(vertices)
        self._positive = positivity
        self.ancestors = []
        self.children = []
    def set_positive(self, value):
        """Sets value for this Poly, as well as for it's children"""
        self._positive = value
        self.update_children()
    def get_positive(self):
        return self._positive
    positive = property(get_positive, set_positive)
    def concentric(self, other):
        """concentric(self, other):
            Returns:
            -1 if self completely enclosed by other,
             1 if self completely encloses other,
             0 if not concentric"""
        tester = array(self.vertices)
        other = array(other.vertices)
        is_in_min  = tester.min(axis=0) > other.min(axis=0)
        is_in_max  = tester.max(axis=0) < other.max(axis=0)
        is_inside = is_in_min[0] and is_in_min[1] and is_in_max[0] and is_in_max[1]
        if is_inside:
            return -1
        else:
            is_out_min  = tester.min(axis=0) < other.min(axis=0)
            is_out_max  = tester.max(axis=0) > other.max(axis=0)
            is_outside = is_out_min[0] and is_out_min[1] and is_out_max[0] and is_out_max[1]
            if is_outside:
                return 1
            else:
                return 0
    def add_child(self, child):
        self.children.append(child)
    def update_children(self):
        val = not self.positive
        for child in self.children:
            child.positive = val
            val = not val
    def add_ancestor(self, ancestor):
        self.ancestors.append(ancestor)
    def update_ancestors(self):
        val = not self.positive
        for ancestor in self.ancestors:
            ancestor.positive = val
            val = not val

def process_segments(segments, runs):
    for seg in segments[1:]:
        success = combine_couplet(seg, runs)
        if not success:
            invert = seg[:]#copy, don't mess up original
            invert.reverse() #try re-ordering, but maintain segements
            success = combine_couplet(invert, runs)
            if not success:
                runs.append([seg])#Create new
    return segments

def combine_couplet(couplet, runs):
    attached = False
    for run in runs:
        i=0
        while not attached and i<len(run):
            if run[i][1] == couplet[0]:
                if len(run) <= i+1:
                    #Is the next point in the run
                    run.append(couplet)
                    attached = True
                else:
                    #Two possibilities:
                    #1. Same segment again, happens a lot, do not repeat segment,
                    #    leave opportunity for shared border polygons by not
                    #    setting as attached
                    #2. Different segmenet comes after, signifying definite
                    #    side-sharing, so again leave attached False
                    #Both cases show opportunity for another poly, so leave unnattached
                    #so that a new run may be generated
                    pass
            i+=1
    return attached

def form_shapes(runs):
    polys = []
    for run in runs:
        new_poly = ConcentricPoly([run[0][0]])
        for couplet in run:
            new_poly.vertices.append(couplet[1])
        print 'new poly', new_poly.vertices
        if len(polys) > 0:
            success = combine_polygons(new_poly, polys)
            if not success:
                polys.append(new_poly)
        else:
            polys.append(new_poly)
    return polys

def combine_polygons(new_poly, polys):
    for poly in polys:
        if new_poly.vertices[0] == poly.vertices[poly.length()-1]:
            #first element in new polygon is last in another
            if new_poly.length()>1:
                poly.add_vertices(new_poly.vertices[1:])#combine elements of polygons
                return True
        elif new_poly.vertices[new_poly.length()-1] == poly.vertices[0]:
            #last element in new polygon equals first in another
            if poly.length()>1:
                poly.set_vertices(new_poly.vertices + poly.vertices[1:])#combine elements, new first
                return True
    return False

def concentracize(polys):
    found_parent = False
    for test in polys:
        for other in polys:
            if len(other.ancestors)==0 and test != other:
                test_val = test.concentric(other)
                if test_val == -1:
                    other.add_child(test)
                    test.add_ancestor(other)
                elif test_val == 1:
                    test.add_child(other)
                    other.add_ancestor(test)
    for poly in polys:
        if len(poly.ancestors) == 0:
            poly.positive = True
    return found_parent

def draw_concentric(dc, cpoly):
    print cpoly.positive
    if cpoly.positive:
        dc.SetBrush(OUT_BRUSH)
    else:
        dc.SetBrush(IN_BRUSH)
    dc.DrawPolygon(cpoly.vertices)

def draw_concentrics(dc, cpolys):
    if type(cpolys) is ConcentricPoly:
        draw_concentric(dc, cpolys)
    else:
        for p in cpolys:
            if len(p.ancestors)==0:
                draw_concentric(dc, p)
                for child in p.children:
                    draw_concentrics(dc, child)

def draw(event):
    couplets = [tri1,tri3] + [tri2, rect1]
    couplets += [rect3, rect2, rect4]
    runs = [[]]
    runs[0].append(couplets[0])  #Initialize the first polygon with the first line

    if len(couplets) > 0:
        couplets = process_segments(couplets,runs)
        print runs
        polys = form_shapes(runs)
        concentracize(polys)
        dc = wx.ClientDC(frm)
        print 'polygons',polys
        for poly in polys:
            dc.DrawPolygon(array(poly.vertices)*(100,100))

def main(event):
    dc = wx.ClientDC(frm)
    import math
    def gen_points(sides, factor, offset=(0,0)):
        points = []
        for m in arange(0, 2*math.pi, (2*math.pi)/sides):
            points.append((math.cos(m), math.sin(m)))
        return (array(points)*factor)+offset

    rect = gen_points(12, 70, (200,200))
    inner = ConcentricPoly(array(rect))
    rect = gen_points(12, 100, (200,200))
    outer = ConcentricPoly(array(rect))
    polys2 = [inner, outer]
    for poly in polys2:
        print "Children:  ", poly.children
        print "Ancestors: ", poly.ancestors
    concentracize(polys2)
    for poly in polys2:
        print "Children:  ", poly.children
        print "Ancestors: ", poly.ancestors
    draw_concentrics(dc, polys2)
    print polys2



frm.draw = main#draw
frm.Bind(wx.EVT_PAINT, frm.draw)
app.MainLoop()

