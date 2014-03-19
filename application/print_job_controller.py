import application.settings as settings
from application.bitmap_viewer import Projector
from application.electronics_interface.arduino_printer import *

class PrintJob(object):
    def __init__(self):
        self.proj = Projector(None, -1, "EDD Projector", (settings.projx, settings.projy), (settings.projw, settings.projh))
        self.proj.Show()
        #self.step_control = PrinterInterface(settings.SERIAL_PORT, settings.LAYER_DEPTH)
        self.proj.bmps_from_dir(settings.PATH + 'generation_buffer/')
    def print_project(self):
        pause = settings.LAYER_CURE_TIME
        #self.step_control.zero()
        for index in range(len(self.proj.slides.bmps)):
            self.proj.set_index(index)
            self.proj.show_current()
            print 'show'
            time.sleep(pause)
            self.proj.clear()
            #self.step_control.next_layer()
    def cleanup(self):
        self.proj.close()
        #self.step_control.destroy()

def main():
    import wx
    app = wx.App()
    p = PrintJob()
    p.print_project()
    p.cleanup()
    app.MainLoop()
if __name__ == '__main__':
    main()
