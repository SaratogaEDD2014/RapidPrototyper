import wx
import application.settings as settings
import time
import random
from application.bitmap_viewer import *
from application.util.app_util import *
from application.util.editors import DynamicDataDisplay

class PrintManager(wx.Panel):
    def __init__(self, parent, id=-1, title="Printing Part", position=wx.DefaultPosition, size=(1450,350)):
        super(PrintManager, self).__init__(parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.defaultBackground)
        w,h = self.GetSize()

        self.cpu = LabeledCPU(self, -1,'Resin Level (mm)', limits=(0,10))
        self.tempGuage= LabeledCPU(self,-1, 'Ambient Temperature',foreground=settings.defaultAccent, limits=(30,120))
        self.clock = DynamicDataDisplay(self, '', size=(w/4,h/7), scale=.6)
        self.bmp_viewer = BMPViewer(self, -1)
        self.bmp_viewer.bmps_from_dir(settings.PATH + 'generation_buffer/')
        self.bmp_viewer.clear()
        top_sizer= wx.GridSizer(1,0)
        meter_sizer = wx.FlexGridSizer(2,2)
        meter_sizer.AddGrowableRow(0)
        meter_sizer.AddGrowableCol(0)
        meter_sizer.AddGrowableCol(1)
        meter_sizer.Add(self.cpu, flag=wx.EXPAND)
        meter_sizer.Add(self.tempGuage, flag=wx.EXPAND)
        meter_sizer.Add(DynamicDataDisplay(self, 'Time Remaining:', size=(w/8,h/10), scale=.6, alignment=wx.ALIGN_RIGHT), flag=wx.EXPAND)
        meter_sizer.Add(self.clock, flag=wx.EXPAND)
        top_sizer.Add(meter_sizer, flag=wx.EXPAND)
        top_sizer.Add(self.bmp_viewer, flag=wx.EXPAND)

        self.gauge = wx.Gauge(self, -1, 10)
        self.gauge_title = DynamicDataDisplay(self, 'Progress 0.0%', size=(w,h/8), scale=.175, alignment=wx.ALIGN_LEFT)
        bottom_panel_sizer = wx.GridSizer(0,1)
        bottom_panel_sizer.Add(self.gauge_title, flag=wx.EXPAND)
        bottom_panel_sizer.Add(self.gauge, flag=wx.EXPAND)

        self.title = TitleBreak(self, -1, size=(w/2,h/4), label=title)
        master_sizer = wx.FlexGridSizer(0, 1)
        master_sizer.Add(self.title, flag=wx.EXPAND)
        master_sizer.AddGrowableRow(1)
        master_sizer.Add(top_sizer, flag=wx.EXPAND)
        master_sizer.Add(bottom_panel_sizer, flag=wx.EXPAND)
        self.SetSizer(master_sizer)

        #timer testing
        wx.CallAfter(self.OnTimer, None)
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def OnTimer(self, event):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        self.clock.SetValue(st)

    #def setTemp()

    def progress(self):
        if self.cpu.value < 100:
            self.gauge.SetValue(self.gauge.GetValue()+1)
            self.gauge.Refresh()
            self.cpu.value = random.randint(0,10)
            self.tempGuage.value = random.randint(30,120)
            self.bmp_viewer.show_next()
            wx.ClientDC(self.gauge_title).Clear()
            self.gauge_title.SetValue('Progress: '+str(self.gauge.GetValue()*100./self.gauge.GetRange()-10)+'%')
            wx.CallLater(1000, self.progress)

#----------------------------------------------------------------------------------
class LabeledCPU(wx.Panel):
    def __init__(self, parent, id=-1, label='', background=settings.defaultBackground, foreground=settings.defaultForeground, limits=(0,100)):
        wx.Panel.__init__(self, parent, id)
        #self.SetBackgroundColour(wx.Colour(1,200,30))
        self.label = DynamicDataDisplay(self, label, scale=.5, foreground=foreground, background=background)
        self.meter = CPU(self, id, background, foreground, limits=limits)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.SendSizeEvent()
    def on_size(self, event):
        w,h = self.GetSize()
        self.label.SetSize((w, h/5))
        self.meter.SetSize((w, (h*4)/5))
        self.meter.SetPosition((0, h/5))
    def set_value(self, num):
        self.meter.value = num
    def get_value(self):
        return self.meter.value
    value = property(get_value, set_value)



class CPU(wx.Panel):
    NUM_RECTS = 20
    def __init__(self, parent, id, background=settings.defaultBackground, foreground=settings.defaultForeground, label=True, limits=(0,100)):
        wx.Panel.__init__(self, parent, id, size=(12,12))
        self.parent = parent
        self.back = background
        self.fore = foreground
        self.label = label
        self.limits = limits
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self._value = 0

    def set_value(self, num):
        self._value = min(self.limits[1], max(self.limits[0], num)) #ensures num is withing range
        self.Refresh()
    def get_value(self):
        return self._value
    value = property(get_value, set_value)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetDeviceOrigin(w/10, (h*9)/10) #Makes lower left corner (0,0)
        dc.SetAxisOrientation(True, True)

        dc.SetBrush(wx.Brush(self.back))
        dc.SetPen(wx.Pen(self.back))
        dc.SetBackground(wx.Brush(self.back))
        dc.Clear()
        pos = self.value
        rect = pos / (float(self.limits[1])/CPU.NUM_RECTS)

        rect_h = h/25
        rect_w = (w*7)/20
        x_1 = w/20
        x_2 = (w*11)/20

        for i in range(1, 21):
            if i > rect:
                dc.SetBrush(wx.Brush(dim_color(self.fore, 80)))
                if self.label == True:
                    if i % (CPU.NUM_RECTS/4) == 0:
                        lim_range = float(self.limits[1]-self.limits[0])
                        text = str(self.limits[0]+i*(lim_range/CPU.NUM_RECTS))
                        draw_text_rect(dc, x_2-rect_w, i*(rect_h-1), rect_w,
                                        rect_h, text, color=self.fore)
                    dc.DrawRectangle(x_2-rect_w/2, i*(rect_h-1), rect_w, rect_h)
                else:
                    dc.DrawRectangle(x_1, i*(rect_h-1), rect_w, rect_h)
                    dc.DrawRectangle(x_2, i*(rect_h-1), rect_w, rect_h)
            else:
                dc.SetBrush(wx.Brush(self.fore))
                if self.label == True:
                    if i % (CPU.NUM_RECTS/4) == 0:
                        lim_range = float(self.limits[1]-self.limits[0])
                        text = str(self.limits[0]+i*(lim_range/CPU.NUM_RECTS))
                        draw_text_rect(dc, x_2-rect_w, i*(rect_h-1), rect_w,
                                        rect_h, text, color=self.fore)
                    dc.DrawRectangle(x_2-rect_w/2, i*(rect_h-1), rect_w, rect_h)
                else:
                    dc.DrawRectangle(x_1, i*(rect_h-1), rect_w, rect_h)
                    dc.DrawRectangle(x_2, i*(rect_h-1), rect_w, rect_h)

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
