import wx
import GUI.settings as settings
from GUI.util.app_util import draw_centered_text
import time

class Splash(wx.Frame):
    def __init__(self, name="Charlie"):
        super(Splash, self).__init__(None, style=wx.NO_BORDER)
        self.CenterOnScreen()
        self.name=name
        self.SetBackgroundColour(settings.button_outside)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetPosition((settings.app_x, settings.app_y))
        self.SetSize((settings.app_w, settings.app_h))
        self.Show(True)


    def on_paint(self, event):
        dc = wx.PaintDC(self)
        text = 'Hello, '
        text_area_factor = .4 #percent of horizontal area available for text
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Trebuchet MS')
        draw_centered_text(self, text, text_area_factor, font, dc)
        time.sleep(1.5)

        dc.Clear()

        text = "I'm " + self.name
        text_area_factor = .7 #percent of horizontal area available for text
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, 'Trebuchet MS')
        draw_centered_text(self, text, text_area_factor, font, dc)
        time.sleep(2)

        self.Close()


def show_splash(name):
    app = wx.App()
    splash = Splash(name)
    app.MainLoop()

if __name__ == '__main__':
    show_splash("Charlie")