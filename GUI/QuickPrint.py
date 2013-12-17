import wx
import AppSettings
#from PartViewer import generate_view

class QuickPrint(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,40), size=wx.Size(800,440)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(AppSettings.secondBackground)
        self.Show(False)
    def Show(self, visible):
        super(QuickPrint, self).Show(visible)
        #if visible:
        #    AppSettings.set_view(generate_view(self))