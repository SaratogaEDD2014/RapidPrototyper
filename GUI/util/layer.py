from numpy import *
import wx

#dir = 'C:/Users/s.krulcik/Documents/Temp/'
directory = 'C:/Users/krulciks14/Pictures'
name = 'size'

def normalize(num, step=.01234):
    """Returns value rounded to nearest increment of step."""
    factor = round(num/step)
    num = step*factor
    return num

class Layer(wx.MemoryDC):
    def __init__(self, z_level, directory, filename, pixel_w=100, pixel_h=100):
        super(Layer, self).__init__();
        zcode = str(int(z_level*1000000))
        self.z = z_level
        self.name = directory + filename + zcode + '.bmp'
        self.bmp = wx.EmptyBitmap(pixel_w, pixel_h)
        self.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        self.SetPen(wx.Pen(wx.Colour(255,255,255)))
        self.SelectObject(self.bmp)
    def save(self):
        self.bmp.SaveFile(self.name, wx.BITMAP_TYPE_BMP)
        print 'save'
    def draw(self, items):
        if len(items)>1:
            if len(items)==6:
                #All three segments are on in the plane
                self.DrawPolygon(items)
            else:
                self.DrawLines(items)
    def Destroy(self):
        self.SelectObject(wx.NullBitmap)
        super(Layer, self).Destroy()
    def demo_draw(self):
        self.DrawRectangle(0,0,50,50)
        self.SetPen(wx.Pen(wx.Colour(0,0,255), 3))
        self.DrawArc(25,25,75,75,50,50)
        self.SetBrush(wx.Brush(wx.Colour(50,190,50)))
        self.DrawCircle(80,80,18)

class LayerManager:
    def __init__(self, layer_step = .012, directory=None, filename=None, pixel_w=100, pixel_h=100):
       """Maintians a list of layer objects and has utilities to manage them"""
       self.name= filename
       self.dir = directory
       self.layers = []
       self.step = layer_step
       self.pixel_w = pixel_w
       self.pixel_h = pixel_h

    def get_layer(self, z):
        """Compares given z to layers. If layer exists, return it; otherwise create lesser layers and desired layers"""
        #Normalize Z
        z = normalize(z, self.step)
        if( z > self.max_z()):
            self.create_layers_below(z)
        else:
            for i in self.layers:
                if i.z == z:
                    return i

    def max_z(self):
        """returns maximum z-value in layers"""
        max = 0
        for i in self.layers:
            if i.z > max:
                max = i.z
        return max

    def create_layers_below(self, z):
        """Given Z, it works backwords to build up layers up to z."""

        # normalize Z
        z = normalize(z)

        startZ = len(self.layers) * self.step
        num_new_layers = (z - startZ) / self.step

        curZ = startZ + self.step
        for i in arange(num_new_layers - 1):
            self.create_layer(curZ)
            curZ += self.step

    def set_layers(self, new_array):
        """Set a new layer list for the object"""
        self.layers = new_array

    def add_layer(self, layer):
        """Add a single layer to layer list"""
        self.layers.append(layer)
    def create_layer(self, z):
        """Instantiates new layer, then adds it to list"""
        new_layer = Layer(z, self.dir, self.name, self.pixel_w, self.pixel_h)
        self.add_layer(new_layer)

    def set_layer(self, z, layer):
        """Replaces a current layer in the list with new one"""
        index = self.layers.index(get_layer(z))
        self.layers[index] = layer




def main():
    app = wx.App()
    manager = LayerManager(.0123, directory, name)
    manager.get_layer(1.0)
    app.MainLoop()
main()
