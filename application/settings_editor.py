##Things I want to be able to edit:
##    All theme colors
##        for now, just choose theme
##    Units for parts
##    Print options:
##        Now:layer thickness
##        Later:Fill Style, speed vs. Strength


##|-----------col1---------|-----------col2---------|
##|                        |                        |
##| -Choose Color Scheme-  |        --Units--       |
##|                        |                        |
##|                        |                        |
##|                        |                        |
##|                        |                        |
##|                        |                        |
##|                        |  --Layer Thickness--   |
##|                        |                        |
##|                        |                        |
##|                        |                        |
##|                        |                        |
##|------------------------|------------------------|


import wx
import application.settings as settings
from application.util.editors import *
from application.util.app_util import *

class SettingsEditor(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,0), size=(settings.app_w, settings.app_h)):
        super(SettingsEditor, self).__init__(parent, id, pos, size)
        self.Show(False)
        self.SetBackgroundColour(settings.defaultBackground)
        master_sizer = wx.FlexGridSizer(0,1)
        content_sizer = wx.GridSizer(1,0, hgap=self.GetSize()[1]/16)
        col1 = wx.GridSizer(0,1, vgap=self.GetSize()[0]/16)
        col2 = wx.GridSizer(0,1, vgap=self.GetSize()[0]/16)

        #Add Base Depth and Support Depth
        #Column 1: the visual appearance stuff
        colors_title = TitleBreak(self, label="Edit Appearance:")
        self.scheme_picker = DynamicComboBox(self, settings.get_scheme(),
                                [key for key in settings.schemes],
                                name="Choose Scheme:", text_color=settings.defaultForeground)
        self.scheme_inverter = LabeledCheckbox(self, name="Inverted Colors", text_color=settings.defaultForeground, size=(self.GetSize()[0], 10))
        self.print_name = LabeledTextEditor(self, -1, settings.get_name(),
                                  name="Printer Name",
                                  text_color=settings.defaultForeground)

        self.user_name = LabeledTextEditor(self, -1, settings.get_user_name(), name="User Name", text_color=settings.defaultForeground)

        col1.Add(colors_title, flag=wx.EXPAND)
        col1.Add(self.scheme_picker, flag=wx.EXPAND)
        col1.Add(self.scheme_inverter, flag=wx.EXPAND)
        col1.Add(self.print_name, flag=wx.EXPAND)
        col1.Add(self.user_name, flag=wx.EXPAND)
        col1.AddMany([wx.Panel(self) for i in range(1)])
        col1.Add(wx.StaticText(self, -1,"***Appearance changes will take effect the next time the application launches."), flag=wx.EXPAND)

        #Column 2: the technical operation settings
        technical_title = TitleBreak(self, label="Print Options:")
        self.unit_selector = DynamicComboBox(self, settings.get_units(),
                                [key for key in settings.unit_factors], name="Units:",
                                text_color=settings.defaultForeground)
        self.layer_depth = LabeledEditor(self, -1, settings.get_layer_depth(),
                                  (0,1), .001, precision=3,name="Layer Thickness",
                                  text_color=settings.defaultForeground)
        self.y_resolution = LabeledEditor(self, -1, settings.projh,
                                  (0,1), .001, precision=1,name="Y Resolution",
                                  text_color=settings.defaultForeground)
        self.x_resolution = LabeledEditor(self, -1, settings.projw,
                                  (0,1), .001, precision=1,name="X Resolution",
                                  text_color=settings.defaultForeground)
        self.layer_cure_time = LabeledEditor(self, -1, settings.get_layer_cure_time(),
                                  (0,1), .001, precision=1,name="Layer Cure Time",
                                  text_color=settings.defaultForeground)

        col2.Add(technical_title, flag=wx.EXPAND)
        col2.Add(self.unit_selector, flag=wx.EXPAND)
        col2.Add(self.layer_depth, flag=wx.EXPAND)
        col2.Add(self.y_resolution, flag=wx.EXPAND)
        col2.Add(self.x_resolution, flag=wx.EXPAND)
        col2.Add(self.layer_cure_time, flag=wx.EXPAND)
        col2.AddMany([wx.Panel(self) for i in range(1)])
        content_sizer.Add(col1, flag=wx.EXPAND)
        content_sizer.Add(col2, flag=wx.EXPAND)
        master_sizer.AddGrowableCol(0)
        master_sizer.Add(TitleBreak(self, label="Edit Settings"), flag=wx.EXPAND)
        master_sizer.AddSpacer(settings.app_h/12)
        master_sizer.AddGrowableRow(2)
        master_sizer.Add(content_sizer, flag=wx.EXPAND)
        self.SetSizer(master_sizer)
        self.SendSizeEvent()

        #event handling
        self.Bind(wx.EVT_COMBOBOX, self.edit_scheme, self.scheme_picker)
        self.Bind(wx.EVT_COMBOBOX, self.edit_scheme, self.scheme_inverter)
        self.Bind(wx.EVT_COMBOBOX, self.edit_resolution, self.y_resolution)
        self.Bind(wx.EVT_COMBOBOX, self.edit_resolution, self.x_resolution)
        self.Bind(wx.EVT_COMBOBOX, self.edit_layer_depth, self.layer_depth)
        self.Bind(wx.EVT_COMBOBOX, self.edit_layer_cure_time, self.layer_cure_time)
        self.Bind(wx.EVT_COMBOBOX, self.edit_name, self.print_name)
        self.Bind(wx.EVT_COMBOBOX, self.edit_user_name, self.user_name)

        #self.Bind(wx.EVT_COMBOBOX, self.edit)

    def edit_scheme(self, event):
        event.Skip()
        settings.set_scheme(self.scheme_picker.GetValue(), self.scheme_inverter.value)
    def edit_resolution(self, event):
        event.Skip()
        settings.set_resolution(self.x_resolution.GetValue(),self.y_resolution.GetValue())
    def edit_layer_depth(self, event):
        event.Skip()
        settings.set_layer_depth(self.layer_depth.GetValue())
    def edit_layer_cure_time(self, event):
        event.Skip()
        settings.set_layer_cure_time(self.layer_cure_time.GetValue())
    def edit_name(self, event):
        event.Skip()
        settings.set_name(self.print_name.GetValue())
    def edit_user_name(self, event):
        event.Skip()
        settings.set_user_name(self.user_name.GetValue())
def main():
    app = wx.App()
    frm = wx.Frame(None, size=(settings.app_w, settings.app_h))
    frm.Show()
    pan=SettingsEditor(frm)
    pan.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()