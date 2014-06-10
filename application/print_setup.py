import application.settings as settings
import wx
from application.bubble_menu import DynamicButtonRect
from application.position_control import *
from application.print_manager import *
from application.util.app_util import color_to_ones
from application.util.editors import *
from application.util.stl import *
from nested_visual import *
from numpy import array
from visual.filedialog import get_file

class STLViewer(wx.Panel):
    def __init__(self, parent, stl_file="", pos=(0,80), size=(settings.app_w,settings.app_h)):
        super(STLViewer, self).__init__(parent, pos=pos, size=size)
        self.Show(False)
        self.file = stl_file
        n = self.file
        n = n.replace('\\', '/')
        n = n[n.rfind('/')+1:]
        self.title_name = n
        self.display = None
        self.part_frame = None
        self.model = None #Holds faces object for part
        self.controls = ControlPanel(self, pos=((size[0]*2)/3, 0), size=(size[0]/3, size[1]-settings.toolbar_h))

        self.Bind(wx.EVT_BUTTON, self.on_print, self.controls.pbutt)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.controls.cbutt)
        self.Bind(wx.EVT_BUTTON, self.on_add_part, self.controls.add_part_butt)

        self.Bind(wx.EVT_BUTTON, self.scale, self.controls.scale_butt)
        self.Bind(wx.EVT_BUTTON, self.rotate, self.controls.rot_butt)
        self.Bind(wx.EVT_BUTTON, self.offset, self.controls.off_butt)

        self.viewer = None
        self.SendSizeEvent()

    def scale(self, event):
        scales = edit_scale()
        settings.SCALE_X = scales[0]
        settings.SCALE_Y = scales[1]
        settings.SCALE_Z = scales[2]
        self.update_model()

    def rotate(self, event):
        rotation = edit_rotation()
        about_x = radians(rotation[0])
        about_y = radians(rotation[1])
        about_z = radians(rotation[2])
        self.part_frame.rotate(angle=about_x, axis=(1,0,0))
        self.part_frame.rotate(angle=about_y, axis=(0,1,0))
        self.part_frame.rotate(angle=about_z, axis=(0,0,1))
        self.update_model()

    def offset(self, event):
        offset = edit_offset()
        settings.OFFSET_X = offset[0]
        settings.OFFSET_Y = offset[1]
        settings.OFFSET_Z = offset[2]
        if self.part_frame != None:
            self.part_frame.pos = (settings.OFFSET_X, settings.OFFSET_Y, settings.OFFSET_Z)

    def Show(self, visible):
        super(STLViewer, self).Show(visible)
        if visible:
            settings.show_visual()
            if self.file != "":
                self.title = label(text=self.title_name, xoffset=0, z=build_h*.75, line=0, pos=(0,0), opacity=0.5)
                self.update_model()
        else:
            settings.hide_visual
            settings.display_part=True
    def destroy_model(self):
        if self.model != None:
            self.model.faces.visible = False
            del self.model.faces
            del self.model
            self.model = None

    def on_add_part(self, event):
        try:
            self.file = select_stl()
            self.update_model()
        except IOError:
            dlg = wx.MessageDialog(self, 'Error: Not a valid filename.', 'Error Opening File', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def update_model(self):
        settings.show_visual()
        settings.environment.add_part_to_display(str(self.file))
    def on_print(self, event):
        dialog = wx.ProgressDialog("Processing "+self.title_name+":", "Process is 10% complete.", 100, self)
        self.model.process_from_faces(dialog)
        dialog.Destroy()
        self.destroy_model()
        print_screen = PrintManager(self.GetParent(), -1, "Print "+self.title_name)
        settings.set_view(print_screen)#Print View Screen
        print_screen.SendSizeEvent()
        print_screen.print_file()

    def on_cancel(self, event):
        self.destroy_model()
        settings.main_v_window.panel.SetSize((1,1))  #Makes display invisible, invoking the private _destroy removes whole window, not just display
        settings.goto_prev_page()


def select_stl():
    dlg = wx.FileDialog(None, message="Choose a file", defaultDir=settings.USER_PATH,
            wildcard='*.stl',style=wx.OPEN | wx.CHANGE_DIR)
    if dlg.ShowModal() == wx.ID_OK:
        name = dlg.GetPath()
        return name
    else:
        return None
    dlg.Destroy()