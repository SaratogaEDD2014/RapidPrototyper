import wx
import GUI.settings as settings

class Splash(wx.Frame):
    def __init__(self, name="Charlie"):
        super(Splash, self).__init__(None, style=wx.NO_BORDER)
        self.CenterOnScreen()
        self.name=name
        self.Maximize(True)
        self.SetBackgroundColour(settings.defaultBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show(True)
        dc = wx.ClientDC(self)
        w,h = self.GetSize()
        dc.SetFont(wx.Font(45, wx.SWISS, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(settings.button_text)
        dc.DrawText(self.name, int((w-len(self.name)*8)/2), int((h-16)/2))



import time
app=wx.App()
splash=Splash()
dc = wx.ClientDC(splash)
w,h = splash.GetSize()
dc.SetFont(wx.Font(45, wx.SWISS, wx.NORMAL, wx.BOLD))
dc.SetTextForeground(settings.button_text)
dc.DrawText(splash.name, int((w-len(splash.name)*8)/2), int((h-16)/2))
time.sleep(3)
splash.Close()
app.MainLoop()