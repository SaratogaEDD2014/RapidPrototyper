import wx
import wx.lib.agw

class LabeledSpin(wx.Panel):
    def __init__(self, parent=None, id=-1, value=0.0, name="Un-named", min=0, max=100, pos=wx.DefaultPosition, size=(180, 20))
        super(SpinControl, self).__init__(parent, id, min=min, max=max, pos=pos, size=size,)
        self.text=wx.StaticText(self, -1, name, (2, 2), (178,18))
        self.control=wx.lib.agw.FloatSpin(self, -1, value=value, min_val=min, max_val=max, pos=(182, 21), size=(178,18))

    def getValue(self):
        return self.control.GetValue()