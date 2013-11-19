import wx
import AppSettings
from GUI.BubbleMenu import *

class TouchSpin(wx.Control):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=wx.DefaultSize, name="NoName"):  #TODO: add style/formatting flags for constructor
        super(TouchSpin, self).__init__(parent, id, pos, size)

        self._value=value
        self._range=limits
        self.increment=increment
        self.name=name
        self._textcontrol=wx.TextCtrl(self, -1, str(self._value), (30, 50), (60, 30))

        h = self._textcontrol.GetSize().height
        w = self._textcontrol.GetSize().width + self._textcontrol.GetPosition().x + 2

        self._up = BubbleButton(self, wx.Bitmap(AppSettings.IMAGE_PATH+'spin_up.png'))
        self._down=BubbleButton(self, wx.Bitmap(AppSettings.IMAGE_PATH+'spin_down.png'))

        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._textcontrol)
        sizer.Add(self._up)
        sizer.Add(self._down)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self._on_click)

    def _on_click(self, event):
        source=event.GetEventObject()
        if self._up is source:
            self.value+=self._inc
        elif self._down is source:
            self.value-=self._inc

    def setValue(self, val):
        self._value=val
        if self._value>self.range[1]:
            self._value=self.range[1]
        elif self._value<self.range[0]:
            self._value=self.range[0]
        self._textcontrol.SetValue(str(self._value))
    def getValue(self):
        return self._value
    value=property(getValue, setValue)

    def setIncrement(self, val):
        self._inc=val
    def getIncrement(self):
        return self._inc
    increment=property(getIncrement, setIncrement)

    def setRange(self, val):
        self._range=val
    def getRange(self):
        return self._range
    range=property(getRange, setRange)


def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=TouchSpin(frm)
    sizer.Add(panel)
    panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
