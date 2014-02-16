import wx
import application.settings as settings
from visual.filedialog import *
from part_viewer import *

class QuickPrint(wx.Panel):
    def __init__(self, parent, stl_file="", id=-1, pos=(0,40), size=wx.Size(800,440)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(settings.defaultBackground)
        self.disp = None
        self.file=stl_file
        self.Show(False)
    def Show(self, visible):
        super(QuickPrint, self).Show(visible)
        if visible:
            try:
                if self.file == "":
                    self.file=get_file()
                    part_viewer = STLViewer(settings.main_window, self.file.name)
                    settings.set_view(part_viewer)
            except IOError:
                dlg = wx.MessageDialog(self, 'Error: Not a valid filename.', 'Error Opening File', wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            super(QuickPrint, self).Show(visible)
            if self.disp != None:
                self.disp._destroy()