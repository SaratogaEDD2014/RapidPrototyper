#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      scott Krulcik
#
# Created:     24/10/2013
#-------------------------------------------------------------------------------
import wx
import wx.lib.plot as plot
import AppSettings

class TemplateEditor(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        super(TemplateEditor, self).__init__(parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(AppSettings.defaultBackground)
        wx.StaticText(self, -1, 'Pitch Diameter:', (20, 20))
        self.sc0 = wx.SpinCtrl(self, -1, str(0), (80, 15), (60, -1))
        wx.StaticText(self, -1, 'Number of Teeth:', (20, 70))
        self.sc1 = wx.SpinCtrl(self, -1, str(0), (80, 15), (60, -1))
        wx.StaticText(self, -1, 'Bore Diameter', (20,70))
        self.sc2 = wx.SpinCtrl(self, -1, str(0), (80, 65), (60, -1))
        wx.Button(self, 1, 'Update', (20, 120))

        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=1)
        self.Centre()

    def OnUpdate(self, event):
        print("Pitch Diameter: ", self.sc0.GetValue())
        print("Number of Teeth", self.sc1.GetValue())
        print("Bore Diameter", self.sc2.GetValue())

class DrawingView(wx.Panel):
    def __init__(self, parent, lines=[plot.PolyLine([(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)])]):
        super(DrawingView, self).__init__(parent)
        self.Show(False)
        self.lines=lines

    def draw(lines):
        self.client = plot.PlotCanvas(self)
        self.gc = plot.PlotGraphics(lines, 'Line Graph', 'X Axis', 'Y Axis')
        self.client.Draw(gc)#,  xAxis= (0,15), yAxis= (0,15))
        self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(client)
        self.SetSizer(self.sizer)

def main():
    ProtoApp = wx.App()
    frame = wx.Frame(None, -1, 'Blue Streaks EDD')
    valueEditor=TemplateEditor(frame)
    display=DrawingView(frame)

    """sizer=wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(display)
    sizer.Add(valueEditor)
    frame.SetSizer(sizer)"""
    valueEditor.Show(True)
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()