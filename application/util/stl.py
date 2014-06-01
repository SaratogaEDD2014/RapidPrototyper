from app_util import normalize, normalize_list, fequal
from geometry_3D import *
from layer import *
from numpy import *
from nested_visual import *
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

class PartFile(object):
    def __init__(self, filename, frm=None):
        self.filename = filename
        self.faces = None
        self.frame = frm

    def process_from_faces(self, dialog=None):
        if self.faces != None:
            #clear bmp storage directory:
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
            basic_name = self.filename[max(self.filename.rfind('/'), self.filename.rfind('\\')):]
            name = basic_name.replace('.stl', '')
            layer_manager = LayerManager(settings.LAYER_DEPTH, BITMAP_DIR, name, settings.BUILD_PIXELS[0], settings.BUILD_PIXELS[1])
            if dialog!=None: dialog.Update(27, 'Generating Facets...')

            #Use faces object to create Facets
            if self.faces == None:
                self.faces = self.generate_faces()
            facets = []
            triplets = array(self.faces.pos).reshape((-1,3))
            for i in arange(0,len(triplets), 3):
                triplets[i] = self.frame.frame_to_world(triplets[i])
                triplets[i+1] = self.frame.frame_to_world(triplets[i+1])
                triplets[i+2] = self.frame.frame_to_world(triplets[i+2])
                if fequal(triplets[i][2], triplets[i+1][2], settings.LAYER_DEPTH/2.) and fequal(triplets[i+1][2], triplets[i+2][2], settings.LAYER_DEPTH/2.):
                    norm = normalize(triplets[i][2], settings.LAYER_DEPTH)
                    triplets[i][2] = norm
                    triplets[i+1][2] = norm
                    triplets[i+2][2] = norm
                facets.append(Facet(triplets[i], triplets[i+1], triplets[i+2]))
            if dialog!=None: dialog.Update(78, 'Slicing '+str(len(facets))+' facets...')
            z1 = normalize(min([facet.min_z() for facet in facets]))
            z2 = normalize(max([facet.max_z() for facet in facets]))
            base_area = wx.Region()
            for z in normalize_list(arange(z2,z1-STEP,-1*STEP)):
                z = round(z,3)
                layer = layer_manager.get_layer(z)
                for facet in facets:
                    level = []
                    for line in (facet.a, facet.b, facet.c):
                        for point in line.calc_xy(z):
                            level.append((int(point[0]*wPPI), int(point[1]*hPPI)))
                    if len(level)>1:
                        if len(level)>=3:
                            #All three segments are on in the plane
                            layer.add_polygon(level)
                        else:
                            layer.add_segment(level)
                layer.support_region = base_area
                layer.prepare()
                base_area.UnionRegion(layer.fill_region)
                base_area.UnionRegion(layer.solid_region)
                base_area.SubtractRegion(layer.empty_region)
                layer.save()
                layer.close()
            for i in arange(0, settings.base_depth/2/STEP, 1):
                #Generate supports to hold part
                layer = Layer(-10, layer_manager.directory, layer_manager.name, layer_manager.pixel_w, layer_manager.pixel_h)
                layer.support_region = base_area
                layer.name = layer_manager.directory + "0    support" + str(int(i)) + ".bmp"
                layer.save()
                layer.close()
            for j in arange(0, settings.base_depth/STEP, 1):
                #Generate solid base for part
                layer = Layer(-10, layer_manager.directory, layer_manager.name, layer_manager.pixel_w, layer_manager.pixel_h)
                r = base_area.Box
                layer.solid_region = wx.Region(r[0],r[1],r[2],r[3])
                layer.name = layer_manager.directory + "0    base" + str(int(j)) + ".bmp"
                layer.save()
                layer.close()
            if dialog!=None: dialog.Update(88, 'Saving bitmaps...')
            if dialog!=None: dialog.Update(100, 'Slicing complete, ready to print.')
            settings.build_bmps = layer_manager.get_bmps()
            return len(facets)

    def generate_faces(self):
        # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
        if isinstance(self.filename, str):
            fd = open(self.filename, mode='rb')
        elif isinstance(self.filename, file):
            if self.filename.mode != 'rb':
                filename = self.filename.name
                self.filename.close()
                fd = open(filename, mode='rb')
            else:
                fd = self.filename
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
                    pass#print ("%d" % (100*n/L))+"%"
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
                    data = [ float(FileLine[1])*settings.x_factor(), float(FileLine[2])*settings.y_factor(), float(FileLine[3])*settings.z_factor() ]
                    triPos.append( data )
            triPos = array(triPos)
            triNor = array(triNor)

        # Compose faces in default frame
        if self.frame == None:
            self.frame = frame()
        self.faces = faces(frame=self.frame, pos=triPos, normal=triNor)

def main():
    part = PartFile(settings.PATH+'examples/temp_file.stl')
    part.generate_faces()
    part.process_from_faces()
    while True:
        rate(200)

if __name__ == '__main__':
    main()
