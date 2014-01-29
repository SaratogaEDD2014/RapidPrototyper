import wx

dir = 'C:/Users/s.krulcik/Documents/Temp/'
name = 'size'

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
        self.SelectObject(wx.NullBitmap)
        self.bmp.SaveFile(self.name, wx.BITMAP_TYPE_BMP)
        self.SelectObject(self.bmp)
    def demo_draw(self):
        self.DrawRectangle(0,0,50,50)
        self.SetPen(wx.Pen(wx.Colour(0,0,255), 3))
        self.DrawArc(25,25,75,75,50,50)
        self.SetBrush(wx.Brush(wx.Colour(50,190,50)))
        self.DrawCircle(80,80,18)
    def close(self):
        self.SelectObject(wx.NullBitmap)

class LayerManager:
    def __init__(self, layer_step = .012, directory=None, filename=None, pixel_w=100, pixel_h=100):
        """Maintians a list of layer objects and has utilities to manage them"""
        self.layers = []
        self.step = layer_step
    def get_layer(self, z):
        """Compares given z to layers. If layer exists, return it; otherwise create lesser layers and desired layers"""
    def max_z(self):
        """returns maximum z-value in layers"""
    def _create_layers_below(self, z):
        """Given Z, it works backwords to build up layers up to z."""
    def set_layers(self, new_array):
        """Set a new layer list for the object"""
    def add_layer(self, layer):
        """Add a single layer to layer list"""
    def create_layer(self, layer):
        """Instantiates new layer, then adds it to list"""
    def set_layer(self, z, layer):
        """Replaces a current layer in the list with new one"""
        

def main():
    app = wx.App()
    layer = Layer(.00123, dir, name)
    layer.demo_draw()
    layer.save()
    app.MainLoop()
main()
