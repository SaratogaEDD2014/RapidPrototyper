#!/usr/bin/python
import wx
import settings as AppSettings
import ProtoToolbar
import MainMenu
from visual import *


class ProtoFrame(window):
    def __init__(self, parent, id, title):
        #super(ProtoFrame, self).__init__(parent, id, title, size=wx.Size(800, 480))
        window.__init__(self, width=800, height=480, title=title)
        self.win.SetBackgroundColour(AppSettings.defaultBackground)
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self.win)
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self.win)
        AppSettings.set_view=self.set_view
        AppSettings.main_window=self
        AppSettings.refresh_view_panel=self.refresh_view_panel
        AppSettings.set_view(self.menu)
        #disp = display(window=AppSettings.main_window, x=15, y=15, width=400, height=400, forward=-vector(0,1,2))
        self.panel=wx.Panel(self.win, pos=(0, 80), size=(800,400))
        self.panel.Show(False)


    def set_view(self, viewPanel):
        if(viewPanel!=None):
            AppSettings.add_prev_page(AppSettings.get_current_page())
            AppSettings.set_current_page(viewPanel)
            AppSettings.refresh_view_panel()
            #self.panel=AppSettings.get_current_page()

    def refresh_view_panel(self):

        mastersizer=wx.BoxSizer(wx.VERTICAL)
        mastersizer.Add(self.toolbar)
        sizer=wx.BoxSizer()
        current=AppSettings.get_current_page()
        sizer.Add(wx.Panel(self.win, size=((800-current.GetSize()[0])/2,20)))
        sizer.Add(current)
        mastersizer.Add(sizer)
        load=wx.Panel(self.win, pos=(0,40), size=(800,400))
        self.win.SetSizer(mastersizer)
        self.win.SendSizeEvent()    #Without this, panels will be misaligned
        load.Destroy()


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    frame.win.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()
