import wx
from App import *
import settings as AppSettings
from visual import *
from PartViewer import generate_view

class QuickPrint(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,40), size=wx.Size(800,440)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(AppSettings.secondBackground)
        self.disp=None
        self.Show(False)
    def Show(self, visible):
        #super(QuickPrint, self).Show(visible)
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


def disp_part():
    disp = display(window=AppSettings.main_window, x=15, y=15, width=400, height=400, forward=-vector(0,1,2))
    cube = box(color=color.red)
    while AppSettings.display_part:
        rate(100)
    disp._destroy()

def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    disp_part()
    frame.win.Show(True)
    frame.panel.Show(False)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()