#!/usr/bin/python
import os
import sys
PATH=os.path.dirname(os.path.realpath(sys.argv[0]))+'/'
sys.path.append(PATH[:PATH.rfind("GUI")])

import GUI.settings as settings
settings.PATH = PATH
settings.IMAGE_PATH = PATH + 'images/'

#Now that things are setup:
import wx
import GUI.splash_screen
import MainMenu
import ProtoToolbar
from nested_visual import *


class ProtoFrame(window):
    def __init__(self, parent, id, title):
        #super(ProtoFrame, self).__init__(parent, id, title, size=wx.Size(800, 480))
        window.__init__(self, width=settings.app_w, height=settings.app_h, x=settings.app_x, y=settings.app_y, title=title)
        settings.icon_view = False #temporary until config file is done
        self.win.Show(False)
        splash = GUI.splash_screen.Splash(settings.NAME)
        splash.say_hi()
        self.win.SetPosition((settings.app_x, settings.app_y))
        self.win.SetSize((settings.app_w, settings.app_h))
        self.win.SetBackgroundColour(settings.defaultBackground)
        self.win.Bind(wx.EVT_PAINT, self.on_paint)
        self.imagePath = settings.IMAGE_PATH+"Main/"
        self.title = title
        self.toolbar = ProtoToolbar.ProtoToolbar(self.win)
        settings.toolbar_h = 40
        self.toolbar.Show(True)
        self.menu = MainMenu.MainMenu(self.win)
        settings.set_view = self.set_view
        settings.main_window = self.win
        settings.main_v_window = self
        settings.set_view(self.menu)
        splash.wait(1)
        splash.say_name()
        splash.wait(1.5)
        self.win.Show(True)
        if settings.icon_view==False:
            self.win.Maximize()
        splash.say_bye()

    def on_paint(self, event):
        event.Skip(True)
        settings.app_w, settings.app_h = self.win.GetSize()
        settings.app_h -= settings.toolbar_h
        app_w = settings.app_w
        app_h = settings.app_h
        self.toolbar.SetSize((app_w, settings.toolbar_h))
        current = settings.get_current_page()
        current.SetSize((app_w, app_h))
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
    main()
