import wx
import GUI.settings as settings

class SupportGenerator(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.Show(False)
        wx.StaticText(self,-1, "SupportGenerator")
        self.SetBackgroundColour(settings.defaultBackground)
