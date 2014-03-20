import wx
import application.settings as settings
import time
import wx.gizmos as gizmos
from util.editors import DynamicDataDisplay
from application.util.app_util import *

class PrintManager(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=(1450,350)):
        super(PrintManager, self).__init__(parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.defaultBackground)
        self.top_panel = wx.Panel(self)
        self.cpu = LabeledCPU(self.top_panel, -1,'Resin Level')
        self.tempGuage= CPU(self.top_panel,-1, foreground=settings.defaultAccent)
        w,h = self.GetSize()

        top_sizer= wx.GridSizer(1,0)
        top_sizer.Add(self.cpu, flag=wx.EXPAND)
        wx.CallAfter(self.OnTimer, None)
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        top_sizer.Add(self.tempGuage, flag=wx.EXPAND)
        top_sizer.Add(wx.StaticText(self.top_panel,-1,"Bitmap"))
        self.top_panel.SetSizer(top_sizer)

        self.bottom_panel = wx.Panel(self)
        self.gauge = wx.Gauge(self.bottom_panel, -1, 10)
        self.clock = DynamicDataDisplay(self.bottom_panel, '', size=(w/8,h/8), scale=.6) #gizmos.LEDNumberCtrl(self.top_panel, -1, wx.DefaultPosition, (200,100), gizmos.LED_ALIGN_CENTER)
        self.gauge_title = wx.Panel(self.bottom_panel)
        bottom_panel_sizer = wx.GridSizer(0,1)
        clock_sizer = wx.GridSizer(1,0)
        clock_sizer.Add(DynamicDataDisplay(self.bottom_panel, 'Time Remaining', size=(w/8,h/10), scale=.6), flag=wx.EXPAND)
        clock_sizer.Add(self.clock, flag=wx.EXPAND)
        clock_sizer.AddSpacer((10,10))
        clock_sizer.AddSpacer((10,10))
        bottom_panel_sizer.Add(clock_sizer, flag=wx.EXPAND)
        bottom_panel_sizer.Add(wx.Panel(self))
        bottom_panel_sizer.Add(self.gauge_title, flag=wx.EXPAND)
        bottom_panel_sizer.Add(self.gauge, flag=wx.EXPAND)
        self.bottom_panel.SetSizer(bottom_panel_sizer)
        #self.bottom_panel.Add(self)

        #self.title = wx.StaticText(self, -1,"PrintManager")

        label_sizer=wx.GridSizer(1,3)
        master_sizer = wx.GridSizer(0, 1)
        label_sizer.Add(DynamicDataDisplay(self,'Resin Level', size=(w/10,h/10), scale=.4), flag=wx.EXPAND)
        #label_sizer.AddSpacer(1)
        label_sizer.Add(DynamicDataDisplay(self,'Temperature', size=(w/10,h/10), scale=.4), flag=wx.EXPAND)
        master_sizer.Add(label_sizer, flag=wx.EXPAND)
        master_sizer.Add(self.top_panel, flag=wx.EXPAND)
        master_sizer.Add(self.bottom_panel, flag=wx.EXPAND)
        self.SetSizer(master_sizer)

    def OnTimer(self, event):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        self.clock.SetValue(st)

    #def setTemp()

    def progress(self):
        if self.cpu.value <=100:
            self.gauge.SetValue(self.gauge.GetValue()+1)
            self.gauge.Refresh()
            self.cpu.value += 10
            self.tempGuage.value +=10
            wx.ClientDC(self.gauge_title).Clear()
            draw_text_left(self.gauge_title, 'Progress: '+str(self.gauge.GetValue()*100./self.gauge.GetRange()-10)+'%', scale=.15, color=settings.defaultForeground)
            wx.CallLater(1000, self.progress)

#----------------------------------------------------------------------------------
class LabeledCPU(wx.Panel):
    def __init__(self, parent, id=-1, label='', background=settings.defaultBackground, foreground=settings.defaultForeground):
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour(wx.Colour(1,200,30))
        self.label = DynamicDataDisplay(self, label, scale=.5)
        self.meter = CPU(self, id, background, foreground)
        self.Bind(wx.EVT_SIZE, self.on_size)
    def on_size(self, event):
        sizer = wx.FlexGridSizer(0, 1)
        w,h = self.GetSize()
        self.label.SetSize((w, h/4))
        sizer.Add(self.label, flag=wx.EXPAND)
        sizer.Add(self.meter, flag=wx.EXPAND)
        sizer.AddGrowableRow(1)
        self.SetSizer(sizer)

    def set_value(self, num):
        self.meter.value = num
    def get_value(self):
        return self.meter.value
    value = property(get_value, set_value)



class CPU(wx.Panel):
    def __init__(self, parent, id, background=settings.defaultBackground, foreground=settings.defaultForeground):
        wx.Panel.__init__(self, parent, id, size=(12,12))
        self.parent = parent
        self.back = background
        self.fore = foreground
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self._value = 0

    def set_value(self, num):
        self._value = num
        self.Refresh()
    def get_value(self):
        return self._value
    value = property(get_value, set_value)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetDeviceOrigin(w/10, (h*9)/10)
        dc.SetAxisOrientation(True, True)

        dc.SetBrush(wx.Brush(self.back))
        dc.SetPen(wx.Pen(self.back))
        dc.DrawRectangle(0,0,(w*8)/10, (h*8)/10)
        pos = self.value
        rect = pos / 5

        for i in range(1, 21):
            if i > rect:
                dc.SetBrush(wx.Brush(dim_color(self.fore, 80)))
                dc.DrawRectangle(10, i*4, 30, 5)
                dc.DrawRectangle(41, i*4, 30, 5)
            else:
                dc.SetBrush(wx.Brush(self.fore))
                dc.DrawRectangle(10, i*4, 30, 5)
                dc.DrawRectangle(41, i*4, 30, 5)

#-----------------------------------------------------------------------------------

def main():
        ProtoApp = wx.App()
        frm = wx.Frame(None, -1, 'Print stuff', size=(800,600))
        panel=PrintManager(frm)
        panel.Show(True)
        frm.Show(True)
        panel.progress()
        ProtoApp.MainLoop()


if __name__ == '__main__':
   main()
