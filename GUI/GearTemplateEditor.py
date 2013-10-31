#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      scott Krulcik
#
# Created:     24/10/2013
#-------------------------------------------------------------------------------
import wx
import plotcopy as plot
import AppSettings

class TemplateEditor(wx.Panel):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.Size(400,400)):
        super(TemplateEditor, self).__init__(parent, id, pos, size)
        #self.Show(False)
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

class DrawingView(plot.PlotCanvas):
    def __init__(self, parent,pos=wx.DefaultPosition, size=(400,400), lines=[plot.PolyLine([(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]),plot.PolyLine([(-4,2), (-2,3), (-1,5), (1,8), (2,8), (4,10)])]):
        super(DrawingView, self).__init__(parent, pos=pos, size=size)
        self.lines=lines

    def defaultDraw(self):
        gc = plot.PlotGraphics(self.lines, 'Gear')
        self.Draw(gc,  xAxis= (0,15), yAxis= (0,15))

def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,450))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    drawing=DrawingView(frm)
    drawing.defaultDraw()
    sizer.Add(drawing)
    sizer.Add(TemplateEditor(frm))

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()