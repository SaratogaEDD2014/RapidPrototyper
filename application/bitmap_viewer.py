import wx
import time
import os
import application.settings as settings

class Projector(wx.Frame):
    #I apologize for the sloppy methods, the inheritance would be screwy for a Frame to extend a Panel type
    def __init__(self, parent, id=-1, title='Projector', pos=(settings.projx, settings.projy), size=(settings.projw, settings.projh)):
        super(Projector, self).__init__(parent, id, title, pos, size, style=wx.NO_BORDER)
        self.slides = BMPViewer(self, -1, size=self.GetSize())
        self.clear()
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
    def show_next(self):
        self.slides.show_next()
    def clear(self):
        self.slides.clear()
    def close(self):
        self.clear()
        del self.slides
        self.Close()


class BMPViewer(wx.Panel):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(BMPViewer, self).__init__(parent, id, pos, size)
        self.SetBackgroundColour(wx.Colour(0,0,0))
        self.bmps = []
        self.index = 0
        self.blank = wx.EmptyBitmap(settings.projw, settings.projh)
    def print_layer_bitmap(self, bmp):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bmp, 0, 0)
    def bmps_from_dir(self, directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            #print file_path
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
        self.index = min(self.index+1, len(self.bmps)-1)
    def show_next(self):
        self.increment_index()
        self.show_current()
    def clear(self):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.blank, 0, 0)


def test():
    import time
    app = wx.App()
    p = Projector(None)#, size=(400,500), pos=(200,0))
    p.Show()

    directory = settings.PATH + 'generation_buffer/'
    p.bmps_from_dir(directory)
    p.clear()
    for i in range(len(p.slides.bmps)):
        p.show_next()
        time.sleep(.25)
    p.clear()
    p.Destroy()
    app.MainLoop()

if __name__ == '__main__':
    test()
    #main()
