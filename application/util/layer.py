import wx
import application.settings as settings
app = wx.App()
from numpy import *
from app_util import normalize, fequal
from shape_parser import *

class Layer(wx.MemoryDC):
    def __init__(self, z_level, directory, filename, pixel_w=100, pixel_h=100):
        super(Layer, self).__init__();
        #ensure all unique 'zcodes' have zeroes out to eight places
        #'zcode' is to be used in filename, so won't save over eachother
        zcode = round(float(z_level), 8)
        zcode = str(zcode)
        while zcode.find('.')<6:
            zcode = '0'+zcode
        zcode = zcode.replace('.','')
        self.z = z_level
        self.name = directory + filename + zcode + '.bmp'
        self.bmp = wx.EmptyBitmap(pixel_w, pixel_h)
        self.SelectObject(self.bmp)
        self.flat_polys = [] #will hold solid polygons, i.e. those that will be completely filled in
        self.segments = [] #Lest of segments created by facets that intersect with layer
        self.polygons = [] #Polygons created by combining segments
        self.solid_region = wx.Region() #Area of positive space (combination of all flat polys in one object)
        self.fill_region = wx.Region()  #Area of positive space that exists between outline of polys, honeycomb
        self.empty_region = wx.Region() #Where no material will be laid. Only inside part, outside of part support structure will be made
        self.support_region = wx.Region() #Area where supports are needed for higher layers
    def add_segment(self, segment):
        if segment not in self.segments:
            self.segments.append(segment)
    def add_segments(self, segments_list):
        for seg in segments_list:
            add_segment(seg)
    def add_polygon(self, poly):
        if len(poly)>0:
            #Eliminate Duplicates
            i = 1
            p2 = poly[0]
            while i<len(poly):
                p1 = p2
                p2 = poly[i]
                if fequal(p1[0], p2[0]) and fequal(p1[1], p2[1]):
                    poly.pop(i)
                else:
                    i+=1
        self.flat_polys.append(poly)
    def prepare(self):
        self.polygons = segments_to_polygons(self.segments)
        self.SetPen(settings.BUILD_PEN)
        concentracize(self.polygons)
        self.create_regions()
    def create_regions(self):
        for poly in self.polygons:
            if poly.positive:
                self.fill_region.UnionRegion(wx.RegionFromPoints(poly.vertices))
            else:
                self.empty_region.UnionRegion(wx.RegionFromPoints(poly.vertices))
        for flat in self.flat_polys:
            self.solid_region.UnionRegion(wx.RegionFromPoints(flat))
    def draw(self):
        self.draw_region(self.support_region, settings.BUILD_SUPPORT)
        self.draw_region(self.empty_region, settings.BUILD_BACKGROUND)
        self.SetPen(wx.Pen(wx.Colour(255,255,255), 3))
        draw_concentrics(self, self.polygons) #Drawn differently to include outline
        self.draw_region(self.solid_region, settings.BUILD_FLAT_BRUSH)
    def draw_region(self, reg, brush):
        self.SetClippingRegionAsRegion(reg)
        self.SetBrush(brush)
        self.DrawRectangleRect(reg.Box)
        self.DestroyClippingRegion()
    def save(self):
        self.draw()
        self.bmp.SaveFile(self.name, wx.BITMAP_TYPE_BMP)
    def clear(self):
        self.segments = []
        self.flat_polys = []
    def demo_draw(self):
        self.DrawRectangle(0,0,50,50)
        self.SetPen(wx.Pen(wx.Colour(0,0,255), 3))
        self.DrawArc(25,25,75,75,50,50)
        self.SetBrush(wx.Brush(wx.Colour(50,190,50)))
        self.DrawCircle(80,80,18)
    def get_z(self):
        return self.z
    def close(self):
        self.clear()
        self.SelectObject(wx.NullBitmap)

class LayerManager:
    def __init__(self, layer_step = .012, directory=None, filename=None, pixel_w=100, pixel_h=100):
        """Maintians a list of layer objects and has utilities to manage them"""
        self.name= filename
        self.directory = directory
        self.layers = []
        self.step = layer_step
        self.pixel_w = pixel_w
        self.pixel_h = pixel_h
        self.max_z = 0
        self.min_z = 0
        self.create_layer(0.0)

    def get_layer(self, z):
        """Compares given z to layers. If layer exists, return it; otherwise create lesser layers and desired layers"""
        #Normalize Z
        z = normalize(z, self.step)
        if z > self.max_z:
            self.create_layers_below(z)
            self.create_layer(z)
            #self.max_z = z #Done automatically in add method
            return self.layers[len(self.layers)-1]
        elif z < self.min_z:
            self.create_layers_above(z)
            self.create_layer(z)
            #self.min_z = z #Done automatically in add method
            return self.layers[0]
        else:
            rel_z = z-self.min_z
            index = int(round(rel_z/self.step))
            return self.layers[index]

    def create_layers_below(self, z):
        """Given Z, it works backwords to build up layers up to z."""
        for layer_value in arange(self.max_z+self.step, z, self.step):
            self.create_layer(layer_value)
    def create_layers_above(self, z):
        """Builds each layer from z lower than min up to min layer."""
        for layer_value in arange(z+self.step, self.min_z, self.step):
            self.create_layer(layer_value)

    def set_layers(self, new_array):
        """Set a new layer list for the object"""
        self.layers = new_array

    def add_layer(self, layer):
        """Add a single layer to layer list"""
        if layer.z > self.max_z:
            self.max_z = layer.z
            self.layers.append(layer)
        elif layer.z < self.min_z:
            self.min_z = layer.z
            self.layers.insert(0, layer)
        else:
            self.layers.insert(len(self.layers)/2, layer)
            self.sort_layers()

    def sort_layers(self):
        """Sorts layers by z-values so their indices can be calculated rather than searched for."""
        self.layers.sort(key=Layer.get_z)

    def create_layer(self, z):
        """Instantiates new layer, then adds it to list"""
        new_layer = Layer(z, self.directory, self.name, self.pixel_w, self.pixel_h)
        new_layer.save()
        self.add_layer(new_layer)

    def set_layer(self, z, layer):
        """Replaces a current layer in the list with new one"""
        i = self.layers.index(get_layer(z))
        self.layers[i] = layer

    def get_bmps(self):
        """Returns a list of bitmaps representing the layers."""
        bmps = []
        for layer in self.layers:
            bmps.append(layer.bmp)
        return bmps


def main():
    directory = settings.PATH + 'generation_buffer/'
    name = 'stuff'

    #layer = Layer(.00123, directory, name)
    tests = [[(635, 417), (538, 461), (538, 461), (537, 457), (537, 457), (635, 417)],
            [(668, 420), (538, 461), (538, 461), (538, 466), (538, 466), (668, 420)],
            [(668, 420), (538, 466), (538, 466), (670, 435), (670, 435), (668, 420)],
            [(668, 420), (670, 435), (670, 435), (538, 466), (538, 466), (668, 420)],
            [(668, 420), (538, 466), (538, 466), (538, 461), (538, 461), (668, 420)],
            [(670, 435), (538, 466), (538, 466), (539, 470), (539, 470), (670, 435)],
            [(670, 435), (539, 470), (539, 470), (642, 454), (642, 454), (670, 435)],
            [(670, 435), (642, 454), (642, 454), (539, 470), (539, 470), (670, 435)],
            [(670, 435), (539, 470), (539, 470), (538, 466), (538, 466), (670, 435)],
            [(642, 454), (539, 470), (539, 470), (539, 475), (539, 475), (642, 454)],
            [(642, 454), (539, 475), (539, 475), (643, 467), (643, 467), (642, 454)],
            [(642, 454), (643, 467), (643, 467), (539, 475), (539, 475), (642, 454)]]

    manager = LayerManager(.12, directory, name, pixel_w=settings.BUILD_PIXELS[0], pixel_h=settings.BUILD_PIXELS[1])
    layer = manager.get_layer(1)
    layer.demo_draw()
    layer.save()
    layer = manager.get_layer(0)
    layer.demo_draw()
    for level in tests:
        layer.DrawPolygon(level)
    layer.save()
    app.MainLoop()
if __name__ == "__main__":
    main()
