import wx
import wx.lib.agw.floatspin as FS

class TouchSpin(wx.Control):
    def __init__(self, parent, id=-1, value=0.0, limits=(0,10), increment=1, pos=wx.DefaultPosition, size=(105,30)):  #TODO: add style/formatting flags for constructor
        super(TouchSpin, self).__init__(parent, id, pos, size)

        self._value=value
        self._textcontrol=wx.TextCtrl(self, -1, "1", (30, 50), (60, -1))

        h = self.text.GetSize().height
        w = self.text.GetSize().width + self.text.GetPosition().x + 2

        self.spin = wx.SpinButton(self, -1,
                                  (w, 50),
                                  (h*2/3, h),
                                  wx.SP_VERTICAL)

        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)

    def _on_click(self, event):
        self.text.SetValue(str(event.GetPosition()))

    def setLimits(self, val):
        self._range=val
    def getLimits(self):
        return self._range
    self.limits=property(getRange, setRange)

    def setValue(self, val):
        self._value=val
    def getValue(self):
        return self._value
    self.value=property(getValue, setValue)

    def setIncrement(self, val):
        self._inc=val
    def getIncrement(self):
        return self._inc
    self.increment=property(getIncrement, setIncrement)
