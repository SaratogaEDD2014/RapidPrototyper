from numpy import *
from app_util import normalize
import wx
import GUI.settings as settings

class Layer(wx.MemoryDC):
    def __init__(self, z_level, directory, filename, pixel_w=100, pixel_h=100):
        super(Layer, self).__init__();
        zcode = str(int(z_level*1000000))
        self.z = z_level
        self.name = directory + filename + zcode + '.bmp'
        self.bmp = wx.EmptyBitmap(pixel_w, pixel_h)
        self.SetBrush(wx.Brush(wx.Colour(255,0,0)))
        self.SelectObject(self.bmp)
    def save(self):
        self.bmp.SaveFile(self.name, wx.BITMAP_TYPE_BMP)
    def demo_draw(self):
        self.DrawRectangle(0,0,50,50)
        self.SetPen(wx.Pen(wx.Colour(0,0,255), 3))
        self.DrawArc(25,25,75,75,50,50)
        self.SetBrush(wx.Brush(wx.Colour(50,190,50)))
        self.DrawCircle(80,80,18)
    def demo_draw(self):
        self.DrawRectangle(0,0,50,50)
        self.SetPen(wx.Pen(wx.Colour(0,255,0), 3))
        self.DrawArc(25,25,75,75,50,50)
        self.SetBrush(wx.Brush(wx.Colour(100,100,255)))
        self.DrawCircle(80,80,18)
    def close(self):
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

    def get_layer(self, z):
        """Compares given z to layers. If layer exists, return it; otherwise create lesser layers and desired layers"""
        #Normalize Z
        z = normalize(z, self.step)
        if z > self.max_z:
            self.create_layers_below(z)
            self.create_layer(z)
        return self.layers[int(round(z/self.step))]

    def get_max(self):
        return len(self.layers)*self.step
    max_z = property(get_max)

    def create_layers_below(self, z):
        """Given Z, it works backwords to build up layers up to z."""
        z = normalize(z, self.step)
        startZ = self.max_z
        for layer_value in arange(startZ, z, self.step):
            self.create_layer(layer_value)

    def set_layers(self, new_array):
        """Set a new layer list for the object"""
        self.layers = new_array

    def add_layer(self, layer):
        """Add a single layer to layer list"""
        if layer.z >= self.max_z:
#            if layer.z != self.layers[len(self.layers)-1].z+self.step:
#                #If there is a gap between max and new highest layer
#                self.create_layers_below(layer.z)
            self.layers.append(layer)
        else:
            for i in range(len(self.layers)-1, -1, -1):
                if layer.z > self.layers[i].z:
                    if layer.z == self.layers[i+1]:
                        #should avoid index out of bounds because of first if in function
                        #This means a layer already exists here
                        self.layers.remove(i+1, layer)
                    self.layers.insert(i+1, layer)


    def create_layer(self, z):
        """Instantiates new layer, then adds it to list"""
        new_layer = Layer(z, self.directory, self.name, self.pixel_w, self.pixel_h)
        new_layer.save()
        print new_layer.z
        self.add_layer(new_layer)
        print len(self.layers)
        print

    def set_layer(self, z, layer):
        """Replaces a current layer in the list with new one"""
        i = self.layers.index(get_layer(z))
        self.layers[i] = layer



def main():
    directory = settings.PATH + 'generation_buffer/'
    name = 'stuff'
    app = wx.App()
    #layer = Layer(.00123, directory, name)
    manager = LayerManager(.12, directory, name)
    layer = manager.get_layer(1)
    layer.demo_draw()
    layer.save()
    layer = manager.get_layer(0)
    layer.demo_draw()
    layer.save()
    app.MainLoop()
main()