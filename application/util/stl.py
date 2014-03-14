from app_util import normalize, normalize_list, fequal
from geometry_3D import *
from layer import *
from numpy import *
from visual import *
import application.settings as settings
import os
import wx

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
def process_file(filename, offsetx=settings.OFFSET_X, offsety=settings.OFFSET_Y, offsetz=settings.OFFSET_Z,dialog=None):
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
                point = (eval(words[1])*settings.x_factor() + offsetx, eval(words[2])*settings.y_factor() + offsety, normalize(eval(words[3])*settings.z_factor() + offsetz, STEP))
                triplet.append(point)
                if len(triplet) == 3:
                    p1,p2,p3 = triplet
                    facets.append(Facet(p1,p2,p3))
                    triplet = []
    if dialog!=None: dialog.Update(78, 'Slicing '+str(len(facets))+' facets...')
    z1 = normalize(min([facet.min_z() for facet in facets]))
    z2 = max([facet.max_z() for facet in facets])
    for z in arange(z1,z2+STEP,STEP):
        layer = layer_manager.get_layer(z)
        for facet in facets:
            level = []
            for line in (facet.a, facet.b, facet.c):
                for point in line.calc_xy(z):
                    level.append((int(point[0]*wPPI), int(point[1]*hPPI)))
            if len(level)>1:
                if len(level)>=6:
                    #All three segments are on in the plane
                    layer.add_polygon(level)
                else:
                    layer.add_segment(level)
        layer.save()
        layer.close()
    if dialog!=None: dialog.Update(88, 'Saving bitmaps...')
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

def stl_to_faces(fileinfo, frm=None): # specify file
    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
    if isinstance(fileinfo, str):
        fd = open(fileinfo, mode='rb')
    elif isinstance(fileinfo, file):
        if fileinfo.mode != 'rb':
            filename = fileinfo.name
            fileinfo.close()
            fd = open(filename, mode='rb')
        else:
            fd = fileinfo
    else:
        raise TypeError, "Specify a file"
    text = fd.read()
    if chr(0) in text: # if binary file
        text = text[84:]
        L = len(text)
        N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
        triNor = zeros((N,3), dtype=float32)
        triPos = zeros((N,3), dtype=float32)
        n = i = 0
        while n < L:
            if n % 200000 == 0:
                print ("%d" % (100*n/L))+"%",
            triNor[i] = fromstring(text[n:n+12], float32)     #Normal Vector
            triPos[i] = fromstring(text[n+12:n+24], float32)*settings.x_factor()
            triPos[i+1] = fromstring(text[n+24:n+36], float32)*settings.y_factor()
            triPos[i+2] = fromstring(text[n+36:n+48], float32)*settings.z_factor()
            colors = fromstring(text[n+48:n+50], uint16)
            if colors != 0:
                print '%x' % colors
            if triNor[i].any():
                triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
            else:
                triNor[i] = triNor[i+1] = triNor[i+2] = \
                    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
            n += 50
            i += 3
    else:
        fd.seek(0)
        fList = fd.readlines()
        triPos = []
        triNor = []

        # Decompose list into vertex positions and normals
        for line in fList:
            FileLine = line.split( )
            if FileLine[0] == 'facet':
                #The definition of the normal vector is found in the "facet" line
                for n in range(3):
                    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
            elif FileLine[0] == 'vertex':
                #These lines define points
                triPos.append( [ float(FileLine[1])*settings.x_factor(), float(FileLine[2])*settings.y_factor(), float(FileLine[3])*settings.z_factor() ]  )
        triPos = array(triPos)
        triNor = array(triNor)

    # Compose faces in default frame
    if frm == None:
        f = frame()
    else:
        f = frm
    return faces(frame=f, pos=triPos, normal=triNor)


"""
    #From Visual Example:---------------------------------------------------------------------------------
    def stl_to_faces(fileinfo): # specify file
    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
    if isinstance(fileinfo, str):
    fd = open(fileinfo, mode='rb')
    elif isinstance(fileinfo, file):
    if fileinfo.mode != 'rb':
    filename = fileinfo.name
    fileinfo.close()
    fd = open(filename, mode='rb')
    else:
    fd = fileinfo
    else:
    raise TypeError, "Specify a file"
    text = fd.read()
    if chr(0) in text: # if binary file
    text = text[84:]
    L = len(text)
    N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
    triNor = zeros((N,3), dtype=float32)
    triPos = zeros((N,3), dtype=float32)
    n = i = 0
    while n < L:
    if n % 200000 == 0:
    print ("%d" % (100*n/L))+"%",
    triNor[i] = fromstring(text[n:n+12], float32)
    triPos[i] = fromstring(text[n+12:n+24], float32)
    triPos[i+1] = fromstring(text[n+24:n+36], float32)
    triPos[i+2] = fromstring(text[n+36:n+48], float32)
    colors = fromstring(text[n+48:n+50], uint16)
    if colors != 0:
    print '%x' % colors
    if triNor[i].any():
    triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
    else:
    triNor[i] = triNor[i+1] = triNor[i+2] = \
    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
    n += 50
    i += 3
    else:
    fd.seek(0)
    fList = fd.readlines()
    triPos = []
    triNor = []

    # Decompose list into vertex positions and normals
    for line in fList:
    FileLine = line.split( )
    if FileLine[0] == 'facet':
    for n in range(3):
    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
    elif FileLine[0] == 'vertex':
    triPos.append( [ float(FileLine[1]), float(FileLine[2]), float(FileLine[3]) ]  )

    triPos = array(triPos)
    triNor = array(triNor)

    # Compose faces in default frame
    f = frame()
    return faces(frame=f, pos=triPos, normal=triNor)

    if __name__ == '__main__':
    #print "Choose an stl file to display. Rotate!"
    # Open .stl file
    while True:
    fd = get_file()
    if not fd: continue

    scene.width = scene.height = 800
    scene.autocenter = True
    newobject = stl_to_faces(fd)
    newobject.smooth() # average normals at a vertex

    # Examples of modifying the returned object:
    ##        newobject.frame.pos = (-1,-1,-0.5)
    ##        newobject.frame.axis = (0,1,0)
    newobject.color = color.orange
    newobject.material = materials.wood
    break"""