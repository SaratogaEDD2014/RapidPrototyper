import wx
import sys
import application.settings
from application.bubble_menu import *
from application.util.calc_dialog import *
from application.util.qwerty_dialog import *
from application.util.app_util import *

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
    def __init__(self, parent, value, pos=wx.DefaultPosition, size=wx.DefaultSize, foreground=settings.defaultForeground, background=settings.defaultBackground, scale=1.4, alignment=wx.ALIGN_CENTER):
        super(DynamicDataDisplay, self).__init__(parent, pos=pos, size=size)#, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(background)
        self.foreground = foreground
        self._value = value
        self.value = value
        self.scale = scale
        self.align = alignment
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
        if self.align == wx.ALIGN_LEFT:
            draw_text_left(self, str(self._value), self.scale, dc=dc, color=self.foreground)
        elif self.align == wx.ALIGN_RIGHT:
            draw_text_right(self, str(self._value), self.scale, dc=dc, color=self.foreground)
        else:
            draw_centered_text(self, str(self._value), self.scale, dc=dc, color=self.foreground)

    #Get and Set with syntax conventions like wx for compatibility in a list of objects
    #Property for more standard python usage
    def SetValue(self, num):
        self._value = num
        self.Refresh()
    def GetValue(self):
        return self._value
    value = property(GetValue, SetValue)

class LabeledEditor(wx.Window):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=wx.DefaultSize, precision=2, name="NoName", text_color=settings.defaultBackground, background_color=None):
        super(LabeledEditor, self).__init__(parent, id, pos, size)
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
        draw_text_left(self.label, self.name, .65, dc=dc, color=self._text_color)

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

class LabeledTextEditor(LabeledEditor):
    def __init__(self, parent, id=-1, value="None", pos=wx.DefaultPosition, size=wx.DefaultSize, name="NoName", text_color=settings.defaultBackground, background_color=None):
        super(LabeledEditor, self).__init__(parent, id, pos, size)
        if background_color == None:
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        else:
            self.SetBackgroundColour(background_color)
        self._value=value  #Will be set again with property to ensure data is updated
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
        self.SetValue(value) #also updates self.data

        self.Bind(wx.EVT_BUTTON, self.on_click)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def SetValue(self, val):
        self._value = val
        self.data.SetValue(self._value)
        self.post()

    def GetValue(self):
        return self._value
    value=property(GetValue, SetValue)

    def on_click(self, event):
        source=event.GetEventObject()
        if self.button is source:
            self.value = text_value(self, 'Edit '+self.name+':', self.value)

class DynamicComboBox(wx.Window):
    def __init__(self, parent, value, choices, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, name="NoName", text_color=settings.defaultBackground):
        super(DynamicComboBox, self).__init__(parent, id, pos, size)
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
        self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.post)

    def post(self, child_event):
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
        draw_text_left(self.label, self.name, .65, dc=dc, color=self._text_color)

    def on_size(self, event):
        event.Skip(True)
        w,h = self.GetSize()
        self.label.SetSize((w/2, h))
        self.box.SetSize((w/5, h))
        self.box.SetPosition(((3*w)/4, 0))

    def SetValue(self, val):
        self.box.SetValue(str(val))
        self.post(wx.CommandEvent())
    def GetValue(self):
        return self.box.GetValue()
    value=property(GetValue, SetValue)

    def SetName(self, val):
        self._name=val
    def GetName(self):
        return self._name
    name=property(GetName, SetName)

class CheckBox(wx.Window):
    def __init__(self, parent, id=-1, initial_value=False, pos=(0,0), size=(10,10), background=settings.defaultBackground, check_color=settings.defaultAccent):
        super(CheckBox, self).__init__(parent, id, pos, size)
        self.SetBackgroundColour(background)
        self.back = background
        self._check_col = check_color
        self.value = initial_value
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    def on_paint(self, event):
        event.Skip()
        w,h = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.back))
        dc.SetPen(wx.Pen(dim_color(self.back), width=w/10))
        dc.DrawRectangle(0,0,w,h)
        if self.value:
            dc.SetPen(wx.Pen(self._check_col, width=w/6))
            points = [(0, h/2), (w/3, h), (w,0)]
            dc.DrawLines(points)
    def post(self):
        event = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, self.GetId())
        event.SetEventObject(self)
        wx.PostEvent(self, event)
    def on_click(self, event):
        self.value = not self.value
    def set_value(self, val):
        self._value = val
        self.Refresh()
        self.post()
    def get_value(self):
        return self._value
    value = property(get_value, set_value)



class LabeledCheckbox(wx.Window):
    def __init__(self, parent, id=-1, initial_value=False, pos=(0,0), size=(settings.app_w/2, settings.app_h/8), name="NoName", text_color=settings.defaultForeground, background_color=settings.defaultBackground):
        super(LabeledCheckbox, self).__init__(parent, id, pos, size)
        self.SetBackgroundColour(background_color)
        w,h = self.GetSize()
        self.name=name
        self._text_color = text_color
        self.label = wx.Window(self) #will eventually hold title
        self.label.SetBackgroundColour(self.GetBackgroundColour())
        self.check_box = CheckBox(self, -1, size=(w/6,h))
        self.value = initial_value

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_CHECKBOX, self.on_click, self.check_box)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Refresh()
    def on_size(self, event):
        event.Skip()
        w,h = self.GetSize()
        self.label.SetSize((w/2, h))
        chk_dim = min(w/6,h)
        self.check_box.SetSize((chk_dim, chk_dim))
        self.check_box.SetPosition(((w*5)/6, 0))
        self.Refresh()
    def on_paint(self, event):
        event.Skip()
        dc = wx.PaintDC(self.label)
        draw_text_left(self.label, self.name, .65, dc=dc, color=self._text_color)
        print 'draw'
    def on_click(self, event):
        self.post()
    def post(self):
        event = wx.CommandEvent(wx.EVT_COMBOBOX.typeId, self.GetId())
        event.SetEventObject(self)
        wx.PostEvent(self, event)
    def set_value(self, val):
        self._value = val
        self.check_box.value = val
        self.post()
    def get_value(self):
        self._value = self.check_box.value
        return self._value
    value = property(get_value, set_value)



def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))
    sizer=wx.GridSizer(0,1)
    touchspin = LabeledEditor(frm, name="hey")
    lblspin = LabeledEditor(frm, name="two", text_color=settings.defaultForeground)
    dynamic = LabeledEditor(frm)
    sizer.Add(touchspin, flag=wx.EXPAND)
    sizer.Add(lblspin, flag=wx.EXPAND)
    sizer.Add(dynamic, flag=wx.EXPAND)
    sizer.Add(LabeledCheckbox(frm, name="Testertest"), flag=wx.EXPAND)
    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()