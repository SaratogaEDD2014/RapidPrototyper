import wx
import settings

class OpenRecent(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(600,380)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.secondBackground)
        sw = wx.ScrolledWindow(self, size=wx.Size(600,380))
        sw.Show(False)
        sizer=wx.GridSizer(5,1,3,3)
        sw.SetScrollbars(20,20,55,40)
        for recent in settings.recentFiles:
            fb=FileBox(self, recent)
            sizer.Add(fb)
            fb.Show(True)
        sw.SetSizer(sizer)
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.GetSizer().Add(sw)
        sw.Show(True)

class FileBox(wx.Panel):
    def __init__(self, parent, filename, id=-1, size=wx.Size(400,100)):
        wx.Panel.__init__(self, parent, id, size=size)
        self.Show(False)
        self.SetBackgroundColour(settings.defaultBackground)
        self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.text=wx.StaticText(self, label=filename)
        self.text.SetForegroundColour(wx.Colour(255,255,255)) # set text color
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticBitmap(self, -1,wx.Bitmap(settings.IMAGE_PATH+"fileIcon.png")))
        sizer.Add(self.text)
        self.SetSizer(sizer)