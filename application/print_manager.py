import wx
import application.settings as settings
import time
import random
from application.bitmap_viewer import *
from application.print_job_controller import *
from application.util.app_util import *
from application.util.editors import DynamicDataDisplay

class PrintManager(wx.Panel):
    def __init__(self, parent, id=-1, title="Printing Part", position=wx.DefaultPosition, size=(settings.app_w,settings.app_h-settings.toolbar_h)):
        super(PrintManager, self).__init__(parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.defaultBackground)
        w,h = self.GetSize()
        self.cpu = LabeledCPU(self, -1,'Resin Level (mm)', limits=(0,10), size=(w/4, h/3))
        self.tempGuage= LabeledCPU(self,-1, 'Ambient Temperature',foreground=settings.defaultAccent, limits=(30,120), size=(w/4, h/3))
        self.clock = DynamicDataDisplay(self, '', size=(w/4,h/7), scale=.6)
        self.bmp_viewer = BMPViewer(self, -1, size=(w/2,h/3))
        self.bmp_viewer.clear()

        top_sizer= wx.GridSizer(1,0)
        meter_sizer = wx.FlexGridSizer(2,2)
        meter_sizer.AddGrowableRow(0)
        meter_sizer.AddGrowableCol(0)
        meter_sizer.AddGrowableCol(1)
        meter_sizer.Add(self.cpu, flag=wx.EXPAND)
        meter_sizer.Add(self.tempGuage, flag=wx.EXPAND)
        meter_sizer.Add(DynamicDataDisplay(self, 'Time Remaining:', size=(w/4,h/10), scale=.6, alignment=wx.ALIGN_RIGHT), flag=wx.EXPAND)
        meter_sizer.Add(self.clock, flag=wx.EXPAND)
        top_sizer.Add(meter_sizer, flag=wx.EXPAND)
        top_sizer.Add(self.bmp_viewer, flag=wx.EXPAND)

        self.gauge = wx.Gauge(self, -1, 100)
        self.gauge_title = DynamicDataDisplay(self, 'Progress 0.0%', size=(w,h/8), scale=.175, alignment=wx.ALIGN_LEFT)
        bottom_panel_sizer = wx.GridSizer(0,1)
        bottom_panel_sizer.Add(self.gauge_title, flag=wx.EXPAND)
        bottom_panel_sizer.Add(self.gauge, flag=wx.EXPAND)

        self.title = TitleBreak(self, -1, size=(w/2,h/6), label=title)
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
        self.print_job = PrintJob(self)

    def print_file(self):
        bmps = settings.build_bmps
        if len(bmps) == 0:
            self.bmp_viewer.bmps_from_dir(settings.PATH+'generation_buffer/')
        else:
            self.bmp_viewer.bmps = bmps
        self.bmp_viewer.index = -1
        self.print_job.print_project()
        #self.print_job.cleanup()

    def OnTimer(self, event):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        self.clock.SetValue(st)

    def progress(self, progress_percent=0, temp=-1, resin=-1):
        self.gauge.SetValue(progress_percent)
        self.gauge.Refresh()
        self.cpu.value = temp
        self.tempGuage.value = resin
        self.bmp_viewer.show_next()
        wx.ClientDC(self.gauge_title).Clear()
        self.gauge_title.SetValue('Progress: '+str(self.gauge.GetValue()*100./self.gauge.GetRange())+'%')
        self.SendSizeEvent()
##        wx.CallLater(1000, self.progress)

#----------------------------------------------------------------------------------
class LabeledCPU(wx.Panel):
    def __init__(self, parent, id=-1, label='', background=settings.defaultBackground, foreground=settings.defaultForeground, limits=(0,100), size=(10,10)):
        wx.Panel.__init__(self, parent, id, size=size)
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
    def __init__(self, parent, id, background=settings.defaultBackground, foreground=settings.defaultForeground, label=True, limits=(0,100), size=(10,10)):
        wx.Panel.__init__(self, parent, id, size=size)
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
        frm = wx.Frame(None, -1, 'Print stuff', size=(settings.app_w, settings.app_h))
        panel=PrintManager(frm)
        frm.Show(True)
        panel.Show(True)
        frm.SendSizeEvent()
        panel.SendSizeEvent()
##        for i in range(100):
##            panel.progress(i, random.randint(0,10), random.randint(30,120))
        panel.print_file()
        ProtoApp.MainLoop()


if __name__ == '__main__':
   main()
