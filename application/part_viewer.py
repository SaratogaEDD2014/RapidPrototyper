import application.settings as settings
import wx
from application.bubble_menu import DynamicButtonRect
from application.util.app_util import color_to_ones, TitleBreak
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

        self.Bind(wx.EVT_COMBOBOX, self.scale, self.controls.scale_x)
        self.Bind(wx.EVT_COMBOBOX, self.scale, self.controls.scale_y)
        self.Bind(wx.EVT_COMBOBOX, self.scale, self.controls.scale_z)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_x)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_y)
        self.Bind(wx.EVT_COMBOBOX, self.offset, self.controls.off_z)

        self.viewer = None
        self.SendSizeEvent()

    def scale(self, event):
        settings.SCALE_X = self.controls.scale_x.GetValue()
        settings.SCALE_Y = self.controls.scale_y.GetValue()
        settings.SCALE_Z = self.controls.scale_z.GetValue()
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
    def on_print(self, event):
        self.dialog = wx.ProgressDialog("Processing "+self.file[self.file.rfind('/'):]+":", "Process is 10% complete.", 100, self)
        process_file(self.file, offsetx=settings.OFFSET_X, offsety=settings.OFFSET_Y, offsetz=settings.OFFSET_Z, dialog = self.dialog)
        self.dialog.Destroy()
    def on_cancel(self, event):
        self.destroy_model()
        settings.main_v_window.panel.SetSize((1,1))  #Makes display invisible, invoking the private _destroy removes whole window, not just display
        settings.goto_prev_page()

class ControlPanel(wx.Panel):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(ControlPanel, self).__init__(parent, id, pos, size)

        w,h = self.GetSize()
        self.v_sizer = wx.GridSizer(0,1)

        top_sizer = wx.GridSizer(1,0)
        self.pbutt = wx.Button(self, label='Print')
        top_sizer.Add(self.pbutt, flag = wx.EXPAND)
        top_sizer.AddSpacer(w/20)
        self.cbutt = wx.Button(self, label='Cancel')
        top_sizer.Add(self.cbutt, flag = wx.EXPAND)
        self.v_sizer.Add(top_sizer, flag=wx.EXPAND)

        scale_sizer = wx.GridSizer(0,1,h/32,0)
        offset_title = TitleBreak(self, size=((2*w)/3, h), label='Scale:')
        scale_sizer.Add(offset_title, flag=wx.EXPAND)
        bl,bw,bh = settings.BUILD_AREA
        self.scale_x = DimensionEditor(self, value=settings.SCALE_X, limits=(-bl,bl),
                                        precision=3, name="X Scale",
                                        text_color=settings.defaultForeground)
        self.scale_y = DimensionEditor(self, value=settings.SCALE_Y, limits=(-bw,bw),
                                        precision=3, name="Y Scale",
                                        text_color=settings.defaultForeground)
        self.scale_z = DimensionEditor(self, value=settings.SCALE_Z, limits=(-bh,bh),
                                        precision=3, name="Z Scale",
                                        text_color=settings.defaultForeground)
        scale_sizer.Add(self.scale_x, flag=wx.EXPAND)
        scale_sizer.Add(self.scale_y, flag=wx.EXPAND)
        scale_sizer.Add(self.scale_z, flag=wx.EXPAND)
        self.v_sizer.Add(scale_sizer, flag=wx.EXPAND)


        bottom_sizer = wx.GridSizer(0,1,h/32,0)
        offset_title = TitleBreak(self, size=((2*w)/3, h), label='Offsets:')
        bottom_sizer.Add(offset_title, flag=wx.EXPAND)
        bl,bw,bh = settings.BUILD_AREA
        self.off_x = DimensionEditor(self, value=0.0, limits=(-bl,bl),
                                        precision=3, name="X Offset",
                                        text_color=settings.defaultForeground)
        self.off_y = DimensionEditor(self, value=0.0, limits=(-bw,bw),
                                        precision=3, name="Y Offset",
                                        text_color=settings.defaultForeground)
        self.off_z = DimensionEditor(self, value=0.0, limits=(-bh,bh),
                                        precision=3, name="Z Offset",
                                        text_color=settings.defaultForeground)
        bottom_sizer.Add(self.off_x, flag=wx.EXPAND)
        bottom_sizer.Add(self.off_y, flag=wx.EXPAND)
        bottom_sizer.Add(self.off_z, flag=wx.EXPAND)
        self.v_sizer.Add(bottom_sizer, flag=wx.EXPAND)

        self.SetSizer(self.v_sizer)
        self.SendSizeEvent()

if __name__ == "__main__":
    import wx

    app = wx.App()
    frm = wx.Frame(None)
    frm.Show()

    pan = ControlPanel(frm)

    app.MainLoop()
