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
        self.win.Bind(wx.EVT_SIZE, self.on_size)
        self.win.Bind(wx.EVT_PAINT, self.on_paint)
        self.imagePath=settings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self.win)
        settings.toolbar_h = 40
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self.win)
        self.current = self.menu
        settings.set_view=self.set_view
        settings.main_window=self.win
        settings.refresh_view_panel=self.refresh_view_panel
        settings.set_view(self.menu)
        self.win.Maximize()
        self.win.Show(True)

    def on_size(self, event):
        event.Skip(True)
        settings.app_w, settings.app_h = self.win.GetSize()

    def on_paint(self, event):
        event.skip()
        app_w = settings.app_w
        app_h = settings.app_h
        self.current.Show(False)
        self.toolbar.Show(False)
        self.toolbar.SetSize((app_w, settings.toolbar_h))
        self.current.SetSize((app_w/2, app_h-toolbar_h))
        x = (app_w-self.current.GetSize()[0])/2     #Calculate explicit centered position, sizers mess things up
        y = toolbar_h
        self.current.SetPosition((x,y))
        self.toolbar.SetSize((app_w, toolbar_h))



    def set_view(self, viewPanel):
        if(viewPanel!=None):
            settings.set_current_page(settings.get_current_page())
            settings.set_current_page(viewPanel)
            self.current = settings.get_current_page()


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    ProtoApp.MainLoop()

if __name__ == '__main__':
    GUI.splash_screen.show_splash(settings.NAME)
    main()
