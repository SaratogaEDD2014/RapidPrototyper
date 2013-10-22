import wx
import AppSettings

class QuickPrint(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        wx.StaticBox(self, -1, "Choose a file", (10, 10), size=(240, 170))
        wx.DirPickerCtrl(self, -1, AppSettings.userFilePath,"Choose a file:",pos=(15,25))
        self.SetBackgroundColour(AppSettings.secondBackground)
