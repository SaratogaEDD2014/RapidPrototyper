import wx

class Layer(wx.MemoryDC):
    def __init__(self, z_level, directory, filename, pixel_w=100, pixel_h=100):
        super(Layer, self).__init__();
        #ensure all 'zcodes' have zeroes out to eight places
        zcode = round(float(z_level), 8)
        zcode = str(zcode)
        while zcode.find('.')<6:
            zcode = '0'+zcode
        zcode = zcode.replace('.','')
        self.z = z_level
        self.name = directory + filename + zcode + '.bmp'
        self.bmp = wx.EmptyBitmap(pixel_w, pixel_h)
        self.SelectObject(self.bmp)
        self.flat_polys = []
        self.segments = []
    def add_segment(self, segment):
        if segment not in self.segments:
            self.segments.append(segment)
    def add_segments(self, segments_list):
        for seg in segments_list:
            add_segment(seg)
    def add_polygon(self, poly):
        self.flat_polys.append(poly)
    def prepare(self):
        polygons = segments_to_polygons(self.segments)
        self.SetPen(wx.Pen(wx.Colour(255,255,255), 3))
        concentracize(polygons)
        draw_concentrics(self, polygons)
        self.SetBrush(settings.BUILD_FLAT_BRUSH)
        for flat in self.flat_polys:
            self.DrawPolygon(flat)
    def save(self):
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

def generate_supports(layers):
    for i in range(len(layers)-1, -1, -1):



if __name__ == '__main__':
    main()