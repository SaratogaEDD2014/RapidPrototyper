import wx
import AppSettings

class SupportGenerator(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        wx.StaticText(self,-1, "SupportGenerator")
        self.SetBackgroundColour(AppSettings.defaultBackground)
