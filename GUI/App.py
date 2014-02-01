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
        window.__init__(self, width=1200, height=700, x=8, y=30, title=title)
        settings.icon_view = False #temporary until config file is done
        self.win.Show(False)
        self.win.SetBackgroundColour(settings.defaultBackground)
        self.win.Bind(wx.EVT_PAINT, self.on_paint)
        self.imagePath=settings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self.win)
        settings.toolbar_h = 40
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self.win)
        settings.set_view=self.set_view
        settings.main_window=self.win
        settings.set_view(self.menu)
        self.win.Show(True)
        if settings.icon_view==False:
            self.win.Maximize()

    def on_paint(self, event):
        event.Skip(True)
        settings.app_w, settings.app_h = self.win.GetSize()
        settings.app_h -= settings.toolbar_h
        app_w = settings.app_w
        app_h = settings.app_h
        self.toolbar.SetSize((app_w, settings.toolbar_h))
        current = settings.get_current_page()
        current.SetSize((app_w, app_h-settings.toolbar_h))
        x = (app_w-current.GetSize()[0])/2     #Calculate explicit centered position, sizers mess things up
        y = settings.toolbar_h
        current.SetPosition((x,y))
        current.Refresh()
        self.toolbar.Refresh()


    def set_view(self, viewPanel):
        if(viewPanel!=None):
            settings.add_prev_page(settings.get_current_page())
            settings.set_current_page(viewPanel)
            self.win.Refresh()


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    ProtoApp.MainLoop()

if __name__ == '__main__':
    GUI.splash_screen.show_splash(settings.NAME)
    main()
