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
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.Size(400,400), numTeeth=25, pitchDistance=.15, pitchDiameter=3.0, bore=1.0):
        super(TemplateEditor, self).__init__(parent, id, pos, size)
        #self.Show(False)
        self.pitchDiameter= pitchDiameter
        self.numTeeth= numTeeth
        self.bore= bore
        self.pitchDistance=pitchDistance
        self.SetBackgroundColour(AppSettings.defaultBackground)
        wx.StaticText(self, -1, 'Pitch Diameter:', (20, 20))
        self.sc0 = wx.SpinCtrl(self, -1, str(0), (120, 15), (60, -1))
        wx.StaticText(self, -1, 'Number of Teeth:', (20, 70))
        self.sc1 = wx.SpinCtrl(self, -1, str(0), (120, 65), (60, -1))
        wx.StaticText(self, -1, 'Bore Diameter', (20,120))
        self.sc2 = wx.SpinCtrl(self, -1, str(0), (120, 115), (60, -1))
        wx.StaticText(self, -1, 'Pitch Distance', (20,170))
        self.sc3 = wx.SpinCtrl(self, -1, str(0), (120, 165), (60, -1))
        wx.Button(self, 1, 'Update', (20, 200))

        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=1)
        self.Centre()

    def OnUpdate(self, event):
        self.pitchDiameter= float(self.sc0.GetValue())
        self.numTeeth= float(self.sc1.GetValue())
        self.bore= float(self.sc2.GetValue())
        self.pitchDistance=float(self.sc3.GetValue())

class DrawingView(plot.PlotCanvas):
    def __init__(self, parent,pos=wx.DefaultPosition, size=(400,400), lines=[plot.PolyLine([(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]),plot.PolyLine([(-4,2), (-2,3), (-1,5), (1,8), (2,8), (4,10)])]):
        super(DrawingView, self).__init__(parent, pos=pos, size=size)
        self.lines=lines

    def SetLines(self, lines):
        self.lines=lines

    def defaultDraw(self):
        gc = plot.PlotGraphics(self.lines, 'Gear')
        self.Draw(gc)#,  xAxis= (0,15), yAxis= (0,15))


def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def GenerateGear(numTeeth, pitchDistance, diameter, bore):
    tri()
    """outerRadius=diameter/2+pitchDistance/2
    innerRadius=diameter/2-pitchDistance/2
    gear=[]
    inc=math.pi/numTeeth/2 #Angle increment
    for theta in drange(0,2*math.pi, inc*2):
        #Get outer two points of first arc of circle
        x=round(outerRadius*math.cos(theta),4)
        y=round(outerRadius*math.sin(theta),4)
        theta+=inc
        x1=round(outerRadius*math.cos(theta),4)
        y1=round(outerRadius*math.sin(theta),4)

        #get outer two points of arc of inner circle
        #theta2=theta+inc
        x2=round(innerRadius*math.cos(theta),4)
        y2=round(innerRadius*math.sin(theta),4)
        theta+=inc
        x3=round(innerRadius*math.cos(theta),4)
        y3=round(innerRadius*math.sin(theta),4)

        #Generate line that returns to tooth from trough
        x4=round(outerRadius*math.cos(theta),4)
        y4=round(outerRadius*math.sin(theta),4)

        #Create tooth of gear
        gear.append(plot.PolyLine([(x,y), (x1,y1)]))#peak
        gear.append(plot.PolyLine([ (x1,y1) , (x2,y2) ]))
        gear.append(plot.PolyLine([(x2,y2), (x3,y3)]))#trough
        gear.append(plot.PolyLine([ (x3,y3) , (x4,y4) ]))

    #generate bore circle
    bore=bore/2 #convert diameter to radius
    boreCircle=[]
    for theta in drange(0,2*math.pi, bore*math.pi/100):
        boreCircle.append((round(bore*math.cos(theta),4), round(bore*math.sin(theta),4)))
    gear.append(plot.PolyLine(boreCircle))

    print(gear)
    return gear"""

shapes={"triangle":tri, "rectangle":rect, "trapezoid":trap}
gearDim={"pitchDiameter":3, "pitchDepth":.25, "bore":1, "numTeeth":25, "shape":"triangle"}

def tri():
    inr=(gearDim["pitchDiameter"]/2) - gearDim["pitchDepth"] #inner radius
    outr=(gearDim["pitchDiameter"]/2) + gearDim["pitchDepth"]#outer radius
    inc=2*math.pi/gearDim["numTeeth"]
    gear=[]
    for theta in range(0, 2*math.pi, inc):
        points=[]
        r=outr
        points.append([math.round(r*trig(theta)) for trig in [math.cos, math.sin]])
        if gearDim["shape"]!="trapezoid":
            #for rect and tri
            theta+=inc/2
            if gearDim["shape"]=="triangle":
                r=inr
        else:
            #trapezoid
            theta+=inc/4
        points.append([math.round(r*trig(theta)) for trig in [math.cos, math.sin]])
        if gearDim["shape"]=="triangle":
            theta+=inc/2
            r=outr
        else:
            r=inr
            if gearDim["shape"]=="trapezoid":
                theta+=inc/4
        points.append([math.round(r*trig(theta)) for trig in [math.cos, math.sin]])
        #done with triangle
        if gearDim["shape"]!="triangle":
            #r is still inr
            if gearDim["shape"]=="trapezoid":
                theta += inc/4
            else:
                theta+=inc/2
            points.append([math.round(r*trig(theta)) for trig in [math.cos, math.sin]])
            if gearDim["shape"]=="trapezoid":
                r=outr
                theta+=inc/4
                points.append([math.round(r*trig(theta)) for trig in [math.cos, math.sin]])
        gear.append(plot.PolyLine(points))
    print(gear)
    return gear


def trap():
    pass

def rect():
    pass


def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,450))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    drawing=DrawingView(frm)
    template=TemplateEditor(frm)
    drawing.lines=GenerateGear(template.numTeeth, template.pitchDistance, template.pitchDiameter, template.bore)
    drawing.defaultDraw()
    sizer.Add(drawing)
    sizer.Add(template)
    butt=wx.Button(frm, 2, 'plot', (20, 120))
    sizer.Add(butt)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
