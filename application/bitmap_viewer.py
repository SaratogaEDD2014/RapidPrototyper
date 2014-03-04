import wx
import os

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
        if self.current_i >0 and self.current_i<len(self.bmps):
            print 'draw'
            dc.DrawBitmap(self.bmps[self.current_i], self.offx,self.offy)
    def bitmaps_from_dir(self, directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                if the_file.count('.bmp') != 0:
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
        if self.current_i >0 and self.current_i<len(self.bmps):
            print 'draw'
            dc.DrawBitmap(self.bmps[self.current_i], self.offx,self.offy)
    def show_next(self):
        self.show_slide(self.current_i+1)
    def slideshow(self, delay=1):
        self.begin()
        for i in range(len(self.bmps)):
            self.show_next()
            wx.Sleep(delay)

app = wx.App()
frm = wx.Frame(None, size=(800,800))
frm.Show(True)

def showoff(event):
    pan = BitmapViewer(frm, size=(800,800), offsety=30)
    pan.SetBackgroundColour(wx.Colour(200,200,255))
    pan.bitmaps_from_dir('C:/Users/krulciks14/Documents/GitHub/RapidPrototyper/application/generation_buffer')
    pan.slideshow(.5)


def main():
    butt = wx.Button(frm, label='start')
    frm.Bind(wx.EVT_BUTTON, showoff)

    app.MainLoop()

if __name__ == '__main__':
    main()
