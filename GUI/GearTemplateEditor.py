#-------------------------------------------------------------------------------
# Name:        GearTemplateEditor
# Purpose:
#
# Author:      scott Krulcik
#
# Created:     24/10/2013
#-------------------------------------------------------------------------------
import wx
import plotcopy as plot
import AppSettings
import math

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
        self.Draw(gc)#,  xAxis= (0,15), yAxis= (0,15))

numTeeth=40
pitchDistance=.2
diameter=2.5 #in inches

def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def GenerateGear(numTeeth, pitchDistance, diameter):
    outerDiameter=diameter+pitchDistance/2
    innerDiameter=diameter-pitchDistance/2
    gear=[]
    inc=math.pi/numTeeth/2 #Angle increment
    for theta in drange(0,2*math.pi, inc*2):
        #Get outer two points of first arc of circle
        x=round(outerDiameter*math.cos(theta),4)
        y=round(outerDiameter*math.sin(theta),4)
        theta+=inc
        x1=round(outerDiameter*math.cos(theta),4)
        y1=round(outerDiameter*math.sin(theta),4)
        
        #get outer two points of arc of inner circle
        #theta2=theta+inc
        x2=round(innerDiameter*math.cos(theta),4)
        y2=round(innerDiameter*math.sin(theta),4)
        theta+=inc
        x3=round(innerDiameter*math.cos(theta),4)
        y3=round(innerDiameter*math.sin(theta),4)
        
        #Create tooth of gear
        gear.append(plot.PolyLine([(x,y), (x1,y1)]))#peak
        gear.append(plot.PolyLine([ (x1,y1) , (x2,y2) ]))
        gear.append(plot.PolyLine([(x2,y2), (x3,y3)]))#trough
        
    print(gear)
    return gear

def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,450))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    drawing=DrawingView(frm)
    drawing.lines=GenerateGear(numTeeth, pitchDistance, diameter)
    drawing.defaultDraw()
    sizer.Add(drawing)
    sizer.Add(TemplateEditor(frm))

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
