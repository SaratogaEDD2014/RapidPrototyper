import wx
import GUI.settings as settings
from App import *
from visual.filedialog import *
from PartViewer import *

class QuickPrint(wx.Panel):
    def __init__(self, parent, stl_file="", id=-1, pos=(0,40), size=wx.Size(800,440)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(AppSettings.secondBackground)
        self.disp=None
        self.Show(False)
    def Show(self, visible):
        super(QuickPrint, self).Show(visible)
        if visible:
            AppSettings.main_window.panel.Show(True)
            self.disp = display(window=AppSettings.main_window, x=0, y=0, width=400, height=400, forward=-vector(0,1,2))
            cube = box(color=color.red)
            #disp.window.win.Set
            while AppSettings.display_part:
                rate(100)
        else:
            super(QuickPrint, self).Show(visible)
            if self.disp != None:
                self.disp._destroy()

def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')

    #disp_part()
    frame.win.Show(True)
    frame.panel.Show(False)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()