#!/usr/bin/python
import wx
import GUI.settings as settings
import ProtoToolbar
import MainMenu
import GUI.splash_screen
from visual import *


class ProtoFrame(window):
    def __init__(self, parent, id, title):
        #super(ProtoFrame, self).__init__(parent, id, title, size=wx.Size(800, 480))
        window.__init__(self, width=800, height=480, x=8, y=30, title=title)
        settings.icon_view = False
        self.win.Show(False)
        self.win.SetBackgroundColour(settings.defaultBackground)
        self.win.Bind(wx.EVT_SIZE, self.OnSize)
        self.imagePath=settings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self.win)
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self.win)
        settings.set_view=self.set_view
        settings.main_window=self
        settings.refresh_view_panel=self.refresh_view_panel
        settings.set_view(self.menu)
        self.win.Maximize()
        self.win.Show(True)

    def OnSize(self, event):
        event.Skip()
        w,h = self.win.GetSize()
        settings.app_w = w
        settings.app_h = h-settings.toolbar_h
        settings.refresh_view_panel()

    def set_view(self, viewPanel):
        if(viewPanel!=None):
            settings.add_prev_page(settings.get_current_page())
            settings.set_current_page(viewPanel)
            settings.refresh_view_panel()
            load=wx.Panel(self.win, pos=(0,0), size=self.win.GetSize())
            self.win.SendSizeEvent()
            load.Destroy()

    def refresh_view_panel(self):
        mastersizer=wx.BoxSizer(wx.VERTICAL)
        self.toolbar.Refresh()
        mastersizer.Add(self.toolbar)
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        current=settings.get_current_page()
        sizer.Add(wx.Panel(self.win, size=((self.win.GetSize()[0]-current.GetSize()[0])/2,20)))
        sizer.Add(current)
        mastersizer.Add(sizer)
        self.win.SetSizer(mastersizer)


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    ProtoApp.MainLoop()

if __name__ == '__main__':
    GUI.splash_screen.show_splash(settings.NAME)
    main()
