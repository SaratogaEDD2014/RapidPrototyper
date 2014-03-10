import wx
import application.settings as settings
from application.util.app_util import TitleBreak
from application.util.editors import *

class ControlPanel(wx.Panel):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(ControlPanel, self).__init__(parent, id, pos, size)

        w,h = self.GetSize()
        self.v_sizer = wx.GridSizer(0,1, h/64)

        top_sizer = wx.GridSizer(1,0)
        self.pbutt = wx.Button(self, label='Print')
        top_sizer.Add(self.pbutt, flag = wx.EXPAND)
        top_sizer.AddSpacer(w/20)
        self.cbutt = wx.Button(self, label='Cancel')
        top_sizer.Add(self.cbutt, flag = wx.EXPAND)
        self.v_sizer.Add(top_sizer, flag=wx.EXPAND)

##        scale_title = TitleBreak(self, size=((2*w)/3, h), label='Scale:')
##        self.v_sizer.Add(scale_title, flag=wx.EXPAND)
##        bl,bw,bh = settings.BUILD_AREA
##        self.scale_x = DimensionEditor(self, value=settings.SCALE_X, limits=(-bl,bl),
##                                        precision=3, name="X Scale",
##                                        text_color=settings.defaultForeground)
##        self.scale_y = DimensionEditor(self, value=settings.SCALE_Y, limits=(-bw,bw),
##                                        precision=3, name="Y Scale",
##                                        text_color=settings.defaultForeground)
##        self.scale_z = DimensionEditor(self, value=settings.SCALE_Z, limits=(-bh,bh),
##                                        precision=3, name="Z Scale",
##                                        text_color=settings.defaultForeground)
##        self.v_sizer.Add(self.scale_x, flag=wx.EXPAND)
##        self.v_sizer.Add(self.scale_y, flag=wx.EXPAND)
##        self.v_sizer.Add(self.scale_z, flag=wx.EXPAND)

        offset_title = TitleBreak(self, size=((2*w)/3, h), label='Offsets:')
        self.v_sizer.Add(offset_title, flag=wx.EXPAND)
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
        self.v_sizer.Add(self.off_x, flag=wx.EXPAND)
        self.v_sizer.Add(self.off_y, flag=wx.EXPAND)
        self.v_sizer.Add(self.off_z, flag=wx.EXPAND)


        self.SetSizer(self.v_sizer)
        self.SendSizeEvent()

class RotateEditor(wx.Dialog):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=((settings.app_w*3)/4, settings.app_h/2)):
        super(RotateEditor, self).__init__(parent, id, "label" ,pos, size)
        self.changed = False #True if changes implemented, and not 'cancelled' before closing
        self.vals = []
        w,h = self.GetSize()
        rot_size = wx.GridSizer(0,1, h/12, w/12)
        rot_title = TitleBreak(self, size=((2*w)/3, h), label='Rotation:')
        rot_size.Add(rot_title, flag=wx.EXPAND)
        self.rot_x = DimensionEditor(self, value=0.0, limits=(-360,360),
                                        precision=3, name="X Rotation",
                                        text_color=settings.defaultForeground)
        self.rot_y = DimensionEditor(self, value=0.0, limits=(-360, 360),
                                        precision=3, name="Y Rotation",
                                        text_color=settings.defaultForeground)
        self.rot_z = DimensionEditor(self, value=0.0, limits=(-360,360),
                                        precision=3, name="Z Rotation",
                                        text_color=settings.defaultForeground)
        rot_size.Add(self.rot_x, flag=wx.EXPAND)
        rot_size.Add(self.rot_y, flag=wx.EXPAND)
        rot_size.Add(self.rot_z, flag=wx.EXPAND)

        buttons = wx.GridSizer(1, 0, hgap=w/10)
        self.cancel = wx.Button(self, -1, 'Cancel')
        self.finish = wx.Button(self, -1, 'Finish')
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)
        self.Bind(wx.EVT_BUTTON, self.on_finish, self.finish)
        buttons.Add(self.cancel, flag=wx.EXPAND)
        buttons.AddSpacer((10,10))
        buttons.AddSpacer((10,10))
        buttons.Add(self.finish, flag=wx.EXPAND)
        rot_size.Add(buttons, flag=wx.EXPAND)

        self.SetSizer(rot_size)
        self.SendSizeEvent()

    def on_cancel(self, event):
        self.Close()
        self.changed = False
    def on_finish(self, event):
        self.Close()
        self.changed = True
        self.refresh_values()
    def refresh_values(self):
        self.vals = []
        self.vals.append(self.rot_x.GetValue())
        self.vals.append(self.rot_y.GetValue())
        self.vals.append(self.rot_z.GetValue())
    def get_values(self):
        self.refresh_values()
        return self.vals


class ScaleEditor(wx.Dialog):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=((settings.app_w*3)/4, settings.app_h/2)):
        super(ScaleEditor, self).__init__(parent, id, "label" ,pos, size)
        self.changed = False #True if changes implemented, and not 'cancelled' before closing
        self.vals = []
        w,h = self.GetSize()
        scale_size = wx.GridSizer(0,1, h/12, w/12)
        scale_title = TitleBreak(self, size=((2*w)/3, h), label='Scale:')
        scale_size.Add(scale_title, flag=wx.EXPAND)
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
        scale_size.Add(self.scale_x, flag=wx.EXPAND)
        scale_size.Add(self.scale_y, flag=wx.EXPAND)
        scale_size.Add(self.scale_z, flag=wx.EXPAND)

        buttons = wx.GridSizer(1, 0, hgap=w/10)
        self.cancel = wx.Button(self, -1, 'Cancel')
        self.finish = wx.Button(self, -1, 'Finish')
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)
        self.Bind(wx.EVT_BUTTON, self.on_finish, self.finish)
        buttons.Add(self.cancel, flag=wx.EXPAND)
        buttons.AddSpacer((10,10))
        buttons.AddSpacer((10,10))
        buttons.Add(self.finish, flag=wx.EXPAND)
        scale_size.Add(buttons, flag=wx.EXPAND)

        self.SetSizer(scale_size)
        self.SendSizeEvent()

    def on_cancel(self, event):
        self.Close()
        self.changed = False
    def on_finish(self, event):
        self.Close()
        self.changed = True
        self.refresh_values()
    def refresh_values(self):
        self.vals = []
        self.vals.append(self.scale_x.GetValue())
        self.vals.append(self.scale_y.GetValue())
        self.vals.append(self.scale_z.GetValue())
    def get_values(self):
        self.refresh_values()
        return self.vals

def edit_scale():
    s = ScaleEditor(None, size=(800,600))
    s.ShowModal()
    vals = s.get_values()
    s.Destroy()
    return vals

def edit_rotation():
    s = RotateEditor(None, size=(800,600))
    s.ShowModal()
    vals = s.get_values()
    s.Destroy()
    return vals



if __name__ == "__main__":
    import wx

    app = wx.App()
##    frm = wx.Frame(None, size=(800,600))
##    frm.Show()
##    pan = ControlPanel(frm, size=(800,600))
    print edit_scale()
    print edit_rotation()
    app.MainLoop()
