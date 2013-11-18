import wx
import wx.lib.agw.floatspin as FS

class TouchSpin(wx.Control):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=wx.DefaultSize):  #TODO: add style/formatting flags for constructor
        super(TouchSpin, self).__init__(parent, id, pos, size)

        self._value=value
        self._range=limits
        self.increment=increment
        self._textcontrol=wx.TextCtrl(self, -1, "1", (30, 50), (60, -1))

        h = self._textcontrol.GetSize().height
        w = self._textcontrol.GetSize().width + self._textcontrol.GetPosition().x + 2

        self._up = wx.Panel(self, size=(30,30))
        self._up.SetBackgroundColour(wx.Colour(0,0,255))
        self._down=wx.Panel(self, size=(30,30))
        self._down.SetBackgroundColour(wx.Colour(255,0,0))

        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._textcontrol)
        sizer.Add(self._up)
        sizer.Add(self._down)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)

    def _on_click(self, event):
        x, y = event.GetPosition()
        print x,y
        if self._up.region.Contains(x, y):
            self.value+=self._inc
        elif self._down.region.Contains(x,y):
            self.value-=self._inc

    def setValue(self, val):
        self._value=val
        if self._value>self.range[1]:
            self._value=self.range[1]
        elif self._value<self.range[0]:
            self._value=self.range[0]
        self._textcontrol.SetValue(self._value)
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
