import wx
import time
import os
import application.settings as settings

class Projector(wx.Frame):
    #I apologize for the sloppy methods, the inheritance would be screwy for a Frame to extend a Panel type
    def __init__(self, parent, id=-1, title='Projector', pos=(settings.projx, settings.projy), size=(settings.projw, settings.projh)):
        super(Projector, self).__init__(parent, id, title, pos, size, style=wx.NO_BORDER)
        self.slides = BMPViewer(self, -1, size=self.GetSize())
    def print_layer_bitmap(self, bmp):
        self.slides.print_layer_bitmap(bmp)
    def bmps_from_dir(self, directory):
        self.slides.bmps_from_dir(directory)
    def slideshow(self, delay=1):
        self.slides.slideshow(delay)
    def set_index(self, i):
        self.slides.set_index(i)
    def show_index(self, index):
        self.slides.show_index(index)
    def show_current(self):
        self.slides.show_current()
    def increment_index(self):
        self.slides.increment_index()


class BMPViewer(wx.Panel):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(BMPViewer, self).__init__(parent, id, pos, size)
        self.SetBackgroundColour(wx.Colour(0,0,0))
        self.bmps = []
        self.index = 0
    def print_layer_bitmap(self, bmp):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bmp, settings.projx, settings.projy)
    def bmps_from_dir(self, directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            self.bmps.append(wx.Bitmap(file_path))
    def slideshow(self, delay=1):
        for b in self.bmps:
            self.print_layer_bitmap(b)
            if delay>0:
                time.sleep(delay)
    def set_index(self, i):
        self.index = i
    def show_index(self, index):
        self.print_layer_bitmap(self.bmps[i])
    def show_current(self):
        self.print_layer_bitmap(self.bmps[self.index])
    def increment_index(self):
        self.index += 1

def test():
    import time
    app = wx.App()
    p = Projector(None, size=(400,500), pos=(200,0))
    p.Show()

    directory = settings.PATH + 'generation_buffer/'
    p.bmps_from_dir(directory)
    for i in range(len(p.slides.bmps)):
        p.show_current()
        p.increment_index()
        time.sleep(1)
    #p.slideshow()

    app.MainLoop()

if __name__ == '__main__':
    test()
    #main()
