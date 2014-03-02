from app_util import normalize, normalize_list, fequal
from geometry_3D import *
from layer import *
from numpy import *
import wx
import application.settings as settings
import os

STEP = settings.LAYER_DEPTH
BITMAP_DIR = settings.PATH + 'generation_buffer/'
wPPI, hPPI = settings.BUILD_PPI

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
    def add_to_bmps(self, manager):
        z1 = normalize(self.min_z(), STEP)
        z2 = normalize(self.max_z(), STEP)
        for z in arange(z1, z2+STEP, STEP):
            layer = manager.get_layer(z)
            level = []
            for line in (self.a, self.b, self.c):
                for point in line.calc_xy(z):
                    level.append((int(point[0]*wPPI), int(point[1]*hPPI)))
            if len(level)>1:
                if len(level)>=6:
                    #All three segments are on in the plane
                    layer.add_polygon(level)
                else:
                    layer.add_segment(level)

#read text stl match keywords to grab the points to build the model
def process_file(filename, offsetx=settings.BUILD_PIXELS[0]/(2*wPPI), offsety=settings.BUILD_PIXELS[1]/(2*hPPI), dialog=None):
    #clear bmp storage directory
    if dialog!=None: dialog.Update(10, 'Deleting Files...')
    if not os.path.exists(BITMAP_DIR):
        os.makedirs(BITMAP_DIR)
    for the_file in os.listdir(BITMAP_DIR):
        file_path = os.path.join(BITMAP_DIR, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
    f = open(filename,'r')
    basic_name = filename[filename.rfind('/'):]
    name = basic_name.replace('.stl', '')
    layer_manager = LayerManager(settings.LAYER_DEPTH, BITMAP_DIR, name, settings.BUILD_PIXELS[0], settings.BUILD_PIXELS[1])
    facets = []
    triplet = []
    if dialog!=None: dialog.Update(27, 'Generating Facets...')
    for line in f.readlines():
        words = line.split()
        if len(words) > 0:
            if words[0] =='vertex':
                #Get the points of the vertex:
                #Normalize the Z component to a valid step layer, so we don't miss horizontal lines or facets
                point = (eval(words[1]) + offsetx, eval(words[2]) + offsety, normalize(eval(words[3]), STEP))
                #print point
                triplet.append(point)
                if len(triplet) == 3:
                    p1,p2,p3 = triplet
                    facets.append(Facet(p1,p2,p3))
                    triplet = []
    if dialog!=None: dialog.Update(78, 'Slicing '+str(len(facets))+' facets...')
    for facet in facets:
        facet.add_to_bmps(layer_manager)
    if dialog!=None: dialog.Update(88, 'Saving bitmaps...')
    for layer in layer_manager.layers:
        layer.save()
    if dialog!=None: dialog.Update(100, 'Slicing complete, ready to print.')
    f.close()
    return len(facets)

def main():
    app = wx.App()
    process_file(settings.PATH+'examples/bottle.stl')
    app.Destroy()

def test():
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