import wx
import wx.lib.agw.floatspin

class LabeledSpin(wx.Panel):
    def __init__(self, parent=None, id=-1, value=0.0, name="Un-named", min=0, max=100, pos=wx.DefaultPosition, size=(180, 20)):
        super(LabeledSpin, self).__init__(parent, id, pos=pos, size=size,)
        self.text=wx.StaticText(self, -1, name, size=(78,18))
        self.control=wx.lib.agw.floatspin.FloatSpin(self, -1, value=value, min_val=min, max_val=max, size=(78,18))
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
    frame = wx.Frame(None, -1, 'Blue Streaks EDD')
    LabeledSpin(frame)
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()