import wx
import GUI.settings as settings

class FileBrowser(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        wx.StaticText(self,-1, "FileBrowser")
        self.SetBackgroundColour(settings.defaultBackground)
