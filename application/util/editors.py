import wx
import sys
import application.settings
from application.bubble_menu import *
from application.util.calc_dialog import *
from application.util.app_util import draw_centered_text, draw_text_left

class TouchSpin(wx.Window):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=wx.DefaultSize, precision=2, name="NoName"):  #TODO: add style/formatting flags for constructor
        super(TouchSpin, self).__init__(parent, id, pos, size)
        if self.GetParent() != None:
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        self._value=value
        self._range=limits
        self._precision=precision
        self.increment=increment
        self._name=name
        self._textcontrol=wx.TextCtrl(self, -1, str(self.value), (30, 50), (60, 24), style=wx.TE_PROCESS_ENTER | wx.TE_RIGHT)
        self._textcontrol.SetEditable(False)

        h = self._textcontrol.GetSize().height
        w = self._textcontrol.GetSize().width + self._textcontrol.GetPosition().x + 2

        self._up = BubbleButton(self, wx.Bitmap(settings.IMAGE_PATH + 'spin_up.png'))
        self._down=BubbleButton(self, wx.Bitmap(settings.IMAGE_PATH + 'spin_down.png'))
        self._edit=BubbleButton(self, wx.Bitmap(settings.IMAGE_PATH + 'edit_bubble.png'))

        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._edit)
        sizer.Add(self._textcontrol)
        sizer.Add(self._up)
        sizer.Add(self._down)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_TEXT_ENTER, self._on_enter)
        self.Bind(wx.EVT_BUTTON, self._on_butt_click)

    def _on_enter(self, event):
        self.value=float(self._textcontrol.GetValue())

    def _on_butt_click(self, event):
        source=event.GetEventObject()
        if self._up is source:
            self.value+=self._inc
        elif self._down is source:
            self.value-=self._inc
        elif self._edit is source:
            self.value=calc_value(self, 'Edit '+self.name+':')

    def SetValue(self, val):
        self._value=float(val)
        if self._value>self.range[1]:
            self._value=self.range[1]
        elif self._value<self.range[0]:
            self._value=self.range[0]
        self._textcontrol.SetValue(str(round(self._value,self._precision)))
    def GetValue(self):
        return round(self._value,self._precision)
    value=property(GetValue, SetValue)

    def SetName(self, val):
        self._name=val
    def GetName(self):
        return self._name
    name=property(GetName, SetName)

    def setIncrement(self, val):
        self._inc=val
    def getIncrement(self):
        return self._inc
    increment=property(getIncrement, setIncrement)

    def SetPrecision(self, val):
        self._precision=val
    def GetPrecision(self):
        return self._precision
    precision=property(GetPrecision, SetPrecision)

    def setRange(self, val):
        self._range=val
    def getRange(self):
        return self._range
    range=property(getRange, setRange)


class LabeledSpin(wx.Panel):
    def __init__(self, parent=None, id=-1, value=0.0, name="Un-named", min=0, max=100, pos=wx.DefaultPosition):
        super(LabeledSpin, self).__init__(parent, id, pos=pos)
        if self.GetParent():
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        self.SetBackgroundColour(settings.defaultAccent)
        self.text=wx.StaticText(self, -1, name)
        self.control=TouchSpin(self, -1, value=value, limits=(min,max))
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text)
        sizer.Add(self.control)
        self.control.Show(True)
        self.SetSizer(sizer)
        self.Show(True)

    def GetValue(self):
        return self.control.GetValue()
    def SetValue(self, val):
        self.control.SetValue(val)

class DynamicDataDisplay(wx.Window):
    def __init__(self, parent, value, pos=wx.DefaultPosition, size=wx.DefaultSize, foreground=settings.defaultForeground, background=settings.defaultBackground):
        super(DynamicDataDisplay, self).__init__(parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(background)
        self.foreground = foreground
        self._value = value
        self.value = value
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def post(self):
        event = wx.CommandEvent(wx.EVT_COMBOBOX.typeId, self.GetId())
        event.SetEventObject(self)
        wx.PostEvent(self, event)

    def on_paint(self, event):
        event.Skip(True)
        if sys.platform.count('win')>0:
            dc = wx.PaintDC(self)
        else:
            dc = wx.ClientDC(self)#On OSX a wxPaintDC does not work here. I am still trying to figure out why
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        draw_centered_text(self, str(self._value), 1.4, dc=dc, color=self.foreground)

    #Get and Set with syntax conventions like wx for compatibility in a list of objects
    #Property for more standard python usage
    def SetValue(self, num):
        self._value = num
        self.Refresh()
    def GetValue(self):
        return self._value
    value = property(GetValue, SetValue)

class DimensionEditor(wx.Window):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=wx.DefaultSize, precision=2, name="NoName", text_color=settings.defaultBackground, background_color=None):
        super(DimensionEditor, self).__init__(parent, id, pos, size)
        if background_color == None:
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        else:
            self.SetBackgroundColour(background_color)
        self._value=value  #Will be set again with property to ensure data is updated
        self._range=limits
        self._precision=precision
        self.increment=increment
        self._name=name
        self._text_color = text_color

        w,h = self.GetSize()
        self.label = wx.Window(self, size=(w/2, h))
        #increase contrast of gradient
        inside_color = dim_color(settings.defaultAccent, -30)
        outside_color = dim_color(settings.defaultAccent, 20)
        self.button = DynamicButtonRect(self, "Edit", inside_color, settings.defaultAccent, outline = settings.defaultAccent)
        self.button.SetSize((w/4, h))
        self.data = DynamicDataDisplay(self, value, size=(w/4,h), background=text_color, foreground=self.GetBackgroundColour())
        self.value = value #also updates self.data

        self.Bind(wx.EVT_BUTTON, self.on_click)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def post(self):
        event = wx.CommandEvent(wx.EVT_COMBOBOX.typeId, self.GetId())
        event.SetEventObject(self)
        wx.PostEvent(self, event)

    def on_paint(self, event):
        event.Skip(True)
        if sys.platform.count('win')>0:
            dc = wx.PaintDC(self.label)
        else:
            dc = wx.ClientDC(self.label)#On OSX a wxPaintDC does not work here. I am still trying to figure out why
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        draw_text_left(self, self.name, .25, dc=dc, color=self._text_color)

    def on_size(self, event):
        event.Skip(True)
        w,h = self.GetSize()
        self.label.SetSize((w/2, h))
        self.button.SetSize((w/5, h))
        self.button.SetPosition(((3*w)/5,0))
        self.data.SetSize((w/5, h))
        self.data.SetPosition(((4*w)/5, 0))

    def on_click(self, event):
        source=event.GetEventObject()
        if self.button is source:
            self.value = calc_value(self, 'Edit '+self.name+':')

    def SetValue(self, val):
        self._value = val
        self.data.SetValue(round(float(self._value),self._precision))
        self.post()
    def GetValue(self):
        return round(float(self._value),self._precision)
    value=property(GetValue, SetValue)

    def SetName(self, val):
        self._name=val
    def GetName(self):
        return self._name
    name=property(GetName, SetName)

    def setIncrement(self, val):
        self._inc=val
    def getIncrement(self):
        return self._inc
    increment=property(getIncrement, setIncrement)

    def SetPrecision(self, val):
        self._precision=val
    def GetPrecision(self):
        return self._precision
    precision=property(GetPrecision, SetPrecision)

    def setRange(self, val):
        self._range=val
    def getRange(self):
        return self._range
    range=property(getRange, setRange)

class DimensionComboBox(wx.Window):
    def __init__(self, parent, value, choices, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, name="NoName", text_color=settings.defaultBackground):
        super(DimensionComboBox, self).__init__(parent, id, pos, size)
        self.BackgroundColour = self.GetParent().GetBackgroundColour()
        self._name=name
        self._text_color = text_color

        w,h = self.GetSize()
        self.label = wx.Window(self, size=(w/2, h))
        #increase contrast of gradient
        self.box = wx.ComboBox(self, value=value, choices=choices)
        self.box.SetSize((w/5, h))
        self.box.SetPosition(((4*w)/5, 0))

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def post(self):
        event = wx.CommandEvent(wx.EVT_COMBOBOX.typeId, self.GetId())
        event.SetEventObject(self)
        wx.PostEvent(self, event)

    def on_paint(self, event):
        event.Skip(True)
        if sys.platform.count('win')>0:
            dc = wx.PaintDC(self.label)
        else:
            dc = wx.ClientDC(self.label)#On OSX a wxPaintDC does not work here. I am still trying to figure out why
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        draw_text_left(self, self.name, .25, dc=dc, color=self._text_color)

    def on_size(self, event):
        event.Skip(True)
        w,h = self.GetSize()
        self.label.SetSize((w/2, h))
        self.box.SetSize((w/5, h))
        self.box.SetPosition(((3*w)/4, 0))

    def SetValue(self, val):
        self.box.SetValue(val)
        self.post()
    def GetValue(self):
        return self.box.GetValue()
    value=property(GetValue, SetValue)

    def SetName(self, val):
        self._name=val
    def GetName(self):
        return self._name
    name=property(GetName, SetName)

def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))
    panel1 = wx.Panel(frm)
    panel1.SetBackgroundColour(wx.Colour(0,255,0))
    mastersizer = wx.GridSizer(1,2)
    panel = wx.Panel(frm)
    sizer=wx.GridSizer(3,1)
    touchspin = DimensionEditor(panel, name="hey")
    lblspin = DimensionEditor(panel, name="two", text_color=settings.defaultForeground)
    dynamic = DimensionEditor(panel)
    sizer.Add(touchspin, flag=wx.EXPAND)
    sizer.Add(lblspin, flag=wx.EXPAND)
    sizer.Add(dynamic, flag=wx.EXPAND)
    panel.SetSizer(sizer)
    mastersizer.Add(panel1, flag=wx.EXPAND)
    mastersizer.Add(panel, flag=wx.EXPAND)
    frm.SetSizer(mastersizer)
    #panel = DynamicDataDisplay(frm, 12, pos=(25,25), size=(100,100))
    #panel.SetBackgroundColour(settings.defaultForeground)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()