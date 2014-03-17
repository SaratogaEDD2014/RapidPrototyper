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

        #Column 1: the visual appearance stuff
        colors_title = TitleBreak(self, label="Edit Appearance:")
        self.scheme_picker = DynamicComboBox(self, settings.get_scheme(),
                                [key for key in settings.schemes],
                                name="Choose Scheme:", text_color=settings.defaultForeground)
        self.scheme_inverter = LabeledCheckbox(self, name="Inverted Colors", text_color=settings.defaultForeground, size=(self.GetSize()[0], 10))
        col1.Add(colors_title, flag=wx.EXPAND)
        col1.Add(self.scheme_picker, flag=wx.EXPAND)
        col1.Add(self.scheme_inverter, flag=wx.EXPAND)
        col1.AddMany([wx.Panel(self) for i in range(3)])
        col1.Add(wx.StaticText(self, -1,"***Appearance changes will take effect the next time the application launches."), flag=wx.EXPAND)

        #Column 2: the technical operation settings
        technical_title = TitleBreak(self, label="Print Options:")
        self.unit_selector = DynamicComboBox(self, settings.get_units(),
                                [key for key in settings.unit_factors], name="Units:",
                                text_color=settings.defaultForeground)
        self.thickness_editor = LabeledEditor(self, -1, settings.LAYER_DEPTH,
                                  (0,1), .001, precision=3,name="Layer Thickness",
                                  text_color=settings.defaultForeground)
        col2.Add(technical_title, flag=wx.EXPAND)
        col2.Add(self.unit_selector, flag=wx.EXPAND)
        col2.Add(self.thickness_editor, flag=wx.EXPAND)
        col2.AddMany([wx.Panel(self) for i in range(4)])

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

    def edit_scheme(self, event):
        event.Skip()
        settings.set_scheme(self.scheme_picker.GetValue(), self.scheme_inverter.value)

def main():
    app = wx.App()
    frm = wx.Frame(None, size=(settings.app_w, settings.app_h))
    frm.Show()
    pan=SettingsEditor(frm)
    pan.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()