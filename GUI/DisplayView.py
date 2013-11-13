import wx
import AppSettings

class DisplayView(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.imagePath=AppSettings.IMAGE_PATH+"DisplayView/"
        wx.StaticText(self, -1, "DisplayView")
        self.SetBackgroundColour(AppSettings.defaultBackground)
