import wx
import GUI.AppSettings
from GUI.BubbleMenu import *
from GUI.util.calc_dialog import *

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

        self._up = BubbleButton(self, wx.Bitmap(AppSettings.IMAGE_PATH + 'spin_up.png'))
        self._down=BubbleButton(self, wx.Bitmap(AppSettings.IMAGE_PATH + 'spin_down.png'))
        self._edit=BubbleButton(self, wx.Bitmap(AppSettings.IMAGE_PATH + 'edit_bubble.png'))

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
            self.value=calc_value('Edit '+self.name+':')

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


def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    touchspin=TouchSpin(frm)
    lblspin=LabeledSpin(frm)
    sizer.Add(touchspin)
    sizer.Add(lblspin)
    #panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()