import wx
import os
import application.settings as settings

class BitmapViewer(wx.Panel):
    def __init__(self, parent, bitmaps=[], id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, offsetx=0, offsety=0):
        super(BitmapViewer, self).__init__(parent, id, pos, size)
        self.bmps = bitmaps
        self.current_i = -1 #index of bmp being displayed (-1 indicates none displayed)
        self.offx, self.offy = offsetx, offsety
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        event.Skip(True)
        dc = wx.PaintDC(self)
        show_slide(self.current_i)
    def bitmaps_from_dir(self, directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                self.bmps.append(wx.Bitmap(file_path))
    def begin(self):
        self.current_i = 0
        self.Refresh()
    def set_current_slide(self, slide_number):
        slide_number = max(slide_number, 0) #Make sure is is >= 0
        slide_number = min(slide_number, len(self.bmps)-1) #Avoid index out of bounds
        self.current_i = slide_number
    def show_slide(self, slide_number):
        self.set_current_slide(slide_number)
        dc = wx.ClientDC(self)
        dc.Clear()
        if self.current_i >0 and self.current_i<len(self.bmps):
            w,h = self.GetSize()
            to_draw = scale_bitmap(self.bmps[self.current_i],w,h)
            dc.DrawBitmap(to_draw, self.offx,self.offy)
    def show_next(self):
        self.show_slide(self.current_i+1)
    def slideshow(self, delay=1):
        self.begin()
        for i in range(len(self.bmps)):
            self.show_next()
            wx.Sleep(1)

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return wx.BitmapFromImage(image)

def prepare():
    """from app"""
    import os
    import sys
    PATH=os.path.dirname(os.path.realpath(sys.argv[0]))+'/'
    sys.path.append(PATH[:PATH.rfind("application")])

    settings.PATH = PATH
    settings.IMAGE_PATH = PATH + 'images/'


def main():
    app = wx.App()
    frm = wx.Frame(None, size=(800,800))
    frm.Show(True)
    prepare()
    def showoff(event):
        pan = BitmapViewer(frm, size=(800,800), offsety=30)
        pan.SetBackgroundColour(wx.Colour(200,200,255))
        pan.bitmaps_from_dir(settings.PATH+'generation_buffer')
        pan.slideshow(.1)

    butt = wx.Button(frm, label='start')
    frm.Bind(wx.EVT_BUTTON, showoff)

    app.MainLoop()

if __name__ == '__main__':
    main()
