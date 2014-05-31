import time
import application.settings as settings
import wx
from application.util.app_util import draw_centered_text

class Splash(wx.Frame):
    HELLO = 1
    NAME = 2
    def __init__(self, name="Charlie"):
        super(Splash, self).__init__(None, style=wx.NO_BORDER)
        self.CenterOnScreen()
        self.name=name
        self.SetBackgroundColour(settings.button_outside)
        self._view_mode = Splash.HELLO
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetPosition((settings.app_x, settings.app_y))
        self.SetSize((settings.app_w, settings.app_h))
        self.Show(True)

    def wait(self, seconds):
        time.sleep(seconds)

    def on_paint(self, event):
        event.Skip(True)
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush(settings.defaultForeground))
        dc.Clear()
        if self._view_mode == Splash.HELLO:
            text = 'Hello, '
            text_area_factor = .4 #percent of horizontal area available for text
            font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Trebuchet MS')
            draw_centered_text(self, text, text_area_factor, font, dc)
        elif self._view_mode == Splash.NAME:
            text = "I'm " + str(self.name)
            text_area_factor = .7 #percent of horizontal area available for text
            font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, 'Trebuchet MS')
            draw_centered_text(self, text, text_area_factor, font, dc)


    def say_bye(self):
        self.Close()
    def say_hi(self):
        self._view_mode = Splash.HELLO
        self.on_paint(wx.PaintEvent())#I have no idea why self.Refresh() didn't work
    def say_name(self):
        self._view_mode = Splash.NAME
        self.on_paint(wx.PaintEvent())#I have no idea why self.Refresh() didn't work


def show_splash(name):
    app = wx.App()
    splash = Splash(name)
    splash.say_hi()
    splash.wait(1.2)
    splash.say_name()
    splash.wait(1)
    splash.say_bye()
    app.MainLoop()

if __name__ == '__main__':
    show_splash("Charlie")