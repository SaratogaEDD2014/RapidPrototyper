import application.settings as settings
import wx
from application.bubble_menu import DynamicButtonRect
from application.position_control import *
from application.util.app_util import color_to_ones
from application.util.editors import *
from application.util.stl import stl_to_faces, process_file
from nested_visual import *
from numpy import array
from visual.filedialog import get_file

class STLViewer(wx.Panel):
    def __init__(self, parent, stl_file="", pos=(0,80), size=(settings.app_w,settings.app_h)):
        super(STLViewer, self).__init__(parent, pos=pos, size=size)
        self.Show(False)
        self.file = stl_file
        self.display = None
        self.part_frame = None
        self.model = None #Holds faces object for part
        self.controls = ControlPanel(self, pos=((size[0]*2)/3, 0), size=(size[0]/3, size[1]-settings.toolbar_h))

        self.Bind(wx.EVT_BUTTON, self.on_print, self.controls.pbutt)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.controls.cbutt)

        self.Bind(wx.EVT_BUTTON, self.scale, self.controls.scale_butt)
        self.Bind(wx.EVT_BUTTON, self.rotate, self.controls.rot_butt)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_x)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_y)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_z)

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
        self.part_frame.axis = vector((0,0,1)).rotate(about_x, (1,0,0))
        self.part_frame.axis = self.part_frame.axis.rotate(about_y, (0,1,0))
        self.part_frame.axis = self.part_frame.axis.rotate(about_z, (0,0,1))
        print self.part_frame.axis
        self.update_model()

    def offset(self, event):
        settings.OFFSET_X = self.controls.off_x.GetValue()
        settings.OFFSET_Y = self.controls.off_y.GetValue()
        settings.OFFSET_Z = self.controls.off_z.GetValue()
        if self.part_frame != None:
            self.part_frame.pos = (settings.OFFSET_X, settings.OFFSET_Y, settings.OFFSET_Z)

    def Show(self, visible):
        super(STLViewer, self).Show(visible)
        if visible:
            if settings.display_part:
                if self.viewer == None:
                    w = settings.main_v_window
                    background = color_to_ones(settings.defaultBackground)
                    foreground = color_to_ones(settings.defaultForeground)
                    self.display = display(window=w, x=0, y=settings.toolbar_h, width=(settings.app_w*2)/3, height=settings.app_h, up=(0,0,1), forward=vector(-1,-1,-1), background=background, foreground=foreground)
                    self.base_frame = frame()
                    self.part_frame = frame()
                    build_l, build_w, build_h = settings.BUILD_AREA
                    build_z = .02
                    self.x_axis = arrow(pos=(0,0,0), axis=(int(build_l*1.2),0,0), shaftwidth=.02, headwidth=.08,color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.x_label = label(text='X', xoffset=1, yoffset= 1, space=0.2, pos=(int(build_l*1.2),0,0), box=False, frame=self.base_frame)
                    self.y_axis = arrow(pos=(0,0,0), axis=(0,int(build_w*1.2),0), shaftwidth=.02, headwidth=.08, color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.y_label = label(text='y', xoffset=1, yoffset= 0, space=0.2, pos=(0,int(build_w*1.2),0), box=False, frame=self.base_frame)
                    self.z_axis = arrow(pos=(0,0,0), axis=(0,0,int(build_h*1.2)), shaftwidth=.02, headwidth=.08, color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.z_label = label(text='Z', xoffset=1, yoffset= 1, space=0.2, pos=(0,0,int(build_h*1.2)), box=False, frame=self.base_frame)
                    self.platform = box(pos=(build_l/2, build_w/2, -build_z/2),
                        length=build_l, width=build_z, height=build_w, opacity=0.2,
                        color=color_to_ones(settings.secondBackground), frame=self.base_frame)
                    w.panel.SetSize(((settings.app_w*2)/3,settings.app_h))
                    w.win.SendSizeEvent()
                settings.display_part = False
                #self.display.autocenter =True
                if self.file != "":
                    self.update_model()
##                    self.label = label(pos=self.model.pos, text=self.file,
##                        xoffset=1, line=0, yoffset=100, space=100,)
                    n = self.file
                    n = n.replace('\\', '/')
                    n = n[n.rfind('/')+1:]
                    self.title = label(text=n, xoffset=0, z=build_h*.75, line=0, pos=(0,0), opacity=0.5)
                    while not settings.display_part:
                        rate(100)

        else:
            settings.display_part=True
    def destroy_model(self):
        if self.model != None:
            self.model.visible = False
            del self.model
            self.model = None

    def update_model(self):
        if self.display != None:
            if self.model != None:
                self.destroy_model()
            self.model = stl_to_faces(file(self.file), self.part_frame)
            self.model.smooth()
            self.display.autocenter = True
    def on_print(self, event):
        self.dialog = wx.ProgressDialog("Processing "+self.file[self.file.rfind('/'):]+":", "Process is 10% complete.", 100, self)
        process_file(self.file, offsetx=settings.OFFSET_X, offsety=settings.OFFSET_Y, offsetz=settings.OFFSET_Z, dialog = self.dialog)
        self.dialog.Destroy()
    def on_cancel(self, event):
        self.destroy_model()
        settings.main_v_window.panel.SetSize((1,1))  #Makes display invisible, invoking the private _destroy removes whole window, not just display
        settings.goto_prev_page()