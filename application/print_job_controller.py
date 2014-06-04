import application.settings as settings
import wx
from application.bitmap_viewer import Projector
from application.electronics_interface.arduino_printer import *

class PrintJob(object):
    def __init__(self, control_panel=None):
        self.proj = Projector(None, -1, "EDD Projector", (settings.projx, settings.projy), (settings.projw, settings.projh))
        self.proj.Show()
        self.controls = control_panel
        self.step_control = DebugArdu()
        #self.step_control = PrinterInterface(settings.SERIAL_PORT, settings.get_layer_depth())

    def print_project(self):
        bmps = settings.build_bmps
        if len(bmps)>0:
            self.proj.slides.bmps = bmps
        else:
            self.proj.bmps_from_dir(settings.PATH + 'generation_buffer/')
        self.num_layers = len(self.proj.slides.bmps)
        self.percent_per_layer = 1./self.num_layers * 100.
        self.step_control.zero()
        self._print_layer(0)

    def _print_layer(self, index):
##        temp = self.step_control.get_temp()
##        resin_level = self.step_control.get_resin()
        if index < self.num_layers:
            self.proj.clear()
            self.step_control.next_layer()
            self.proj.set_index(index)
            self.proj.show_current()
            current_prog = self.percent_per_layer*(index+1)
            self.controls.progress(current_prog)#, temp, resin_level)
            if index+1 < self.num_layers:
                wx.FutureCall(settings.get_layer_cure_time()*1000, self._print_layer, (index+1))
            else:
                wx.FutureCall(settings.get_layer_cure_time()*1000, self.cleanup)

    def cleanup(self):
        self.proj.close()
        self.step_control.destroy()

class DebugArdu():
    def zero(self):
        pass
    def next_layer(self):
        time.sleep(.1)
        pass
    def destroy(self):
        pass

def main():
    import wx
    app = wx.App()
    p = PrintJob()
    p.print_project()
    p.cleanup()
    app.MainLoop()
if __name__ == '__main__':
    main()
