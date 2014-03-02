import wx
from numpy import *
from application.settings import BUILD_FILL, BUILD_BACKGROUND

OUT_BRUSH = BUILD_FILL
IN_BRUSH = BUILD_BACKGROUND

class Polygon(object):
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
    def get_positive(self):
        return self._positive
    positive = property(get_positive, set_positive)
    def concentric(self, other):
        """concentric(self, other):
            Returns:
            -1 if self completely enclosed by other,
             1 if self completely encloses other,
             0 if not concentric"""
        my_region = wx.RegionFromPoints(self.vertices)
        other_region = wx.RegionFromPoints(other.vertices)
        for p in self.vertices:
            if not other_region.ContainsPoint(p):
                for p2 in other.vertices:
                    if not my_region.ContainsPoint(p2):
                        return 0
                return 1
        return -1
##        tester = array(self.vertices)
##        other = array(other.vertices)
##        is_in_min  = tester.min(axis=0) > other.min(axis=0)
##        is_in_max  = tester.max(axis=0) < other.max(axis=0)
##        is_inside = is_in_min[0] and is_in_min[1] and is_in_max[0] and is_in_max[1]
##        if is_inside:
##            return -1
##        else:
##            is_out_min  = tester.min(axis=0) < other.min(axis=0)
##            is_out_max  = tester.max(axis=0) > other.max(axis=0)
##            is_outside = is_out_min[0] and is_out_min[1] and is_out_max[0] and is_out_max[1]
##            if is_outside:
##                return 1
##            else:
##                return 0
    def add_child(self, child):
        self.children.append(child)
    def update_children(self):
        for child in self.children:
            if len(child.ancestors)%2 == 0:
                child.positive = self.positive
            else:
                child.positive = not self.positive
    def add_ancestor(self, ancestor):
        if not ancestor in self.ancestors:
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
            invert = (seg[1], seg[0])
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
            if test!= other: #len(other.ancestors)==0 and test != other:
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
            poly.update_children()
    return found_parent

def draw_concentric(dc, cpoly):
    if cpoly.positive:
        dc.SetBrush(OUT_BRUSH)
    else:
        dc.SetBrush(IN_BRUSH)
    dc.DrawPolygon(cpoly.vertices)

def draw_concentrics(dc, cpolys):
    new_polys = sorted(cpolys[:], cmp=lambda x,y:cmp(len(x.ancestors), len(y.ancestors)))
    for i in new_polys:
        draw_concentric(dc, i)

def segments_to_polygons(couplets):
    """Given a list of segments, organize them into polygons."""
    if len(couplets) > 0:
        runs = [[]]
        runs[0].append(couplets[0])  #Initialize the first polygon with the first line
        couplets = process_segments(couplets,runs)
        polys = form_shapes(runs)
        return polys
    return []