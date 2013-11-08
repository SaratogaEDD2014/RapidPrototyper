#-------------------------------------------------------------------------------
# Name:        GearTemplate
# Purpose:     This is a panel for generating a gear. It contains window objects to edit parameters and can return a list of points representing the gear object
#
# Author:      Scott Krulcik
#
# Created:     11/2013
#-------------------------------------------------------------------------------

#Scott Krulcik 10/29

import PartTemplate
import math
import wx
import GUI.AppSettings as AppSettings
import GUI.util.plot as plot
import wx.lib.agw.floatspin as fs

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class GearTemplate(wx.Panel):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="trapezoid"):
        super(GearTemplate, self).__init__(parent, size=(800,400))
        self.lines=[]
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions

        self.editors=self.makeEditors()
        self.updateButton=wx.Button(self, 1, 'Update')
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=1)

        self.setDim("Number of Teeth", numTeeth)
        self.setDim("Pitch Diameter",pitchDiameter)
        self.setDim("Bore Diameter",bore)
        self.setDim("Thickness",thickness)
        self.setDim("Tooth Shape",shape)
        self.setHubDim("Thickness",hubThickness)
        self.setHubDim("Hub Diameter",hubDiameter)
        self.makeGear()

        self.display= plot.PlotCanvas(self, pos=wx.DefaultPosition, size=(400,400))
        #self.display.SetBackgroundColour(AppSettings.secondForeground)

        masterSizer=wx.BoxSizer(wx.HORIZONTAL)
        editorSizer=wx.BoxSizer(wx.VERTICAL)
        for e in self.editors:
            editorSizer.Add(e)
        editorSizer.Add(self.updateButton)
        masterSizer.Add(self.display)
        masterSizer.Add(editorSizer)
        self.SetSizer(masterSizer)
        self.OnUpdate(None)

    def OnUpdate(self, event):
        self.makeGear()
        self.grid = plot.PlotGraphics(self.lines, 'Custom Gear')
        self.display.Draw(self.grid)

    def setLines(self, nlines):
        self.lines=nlines

    def getLines(self):
        return self.lines

    def addLines(self, nlines):
        self.lines.append(nlines)

    def getDim(self, key):
        if key in self.gearDim:
            return self.gearDim[key].GetValue()
        else:
            return None

    def getHubDim(self, key):
        if key in self.hubDim:
            return self.hubDim[key].GetValue()
        else:
            return None

    def setDim(self, key, val):
        if key in self.gearDim:
            self.gearDim[key].SetValue(val)
        else:
            pass

    def setHubDim(self, key, val):
        if key in self.hubDim:
            self.hubDim[key].SetValue(val)
        else:
            pass

    def makeGear(self):
        pitch = self.getDim("Number of Teeth")/self.getDim("Pitch Diameter")
        addendum = 1 /  pitch
        dedendum = 1.157 / pitch
        inr=(self.getDim("Pitch Diameter")/2.0) - dedendum #inner radius
        outr=(self.getDim("Pitch Diameter")/2.0) + addendum #outer radius
        inc=2*math.pi/self.getDim("Number of Teeth")
        gear=[]
        points=[]
        for theta in drange(-inc/2, 2*math.pi-inc/2, inc):
            r=outr
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if self.getDim("Tooth Shape")!="trapezoid":
                #for rect and tri
                theta+=inc/2.0
                if self.getDim("Tooth Shape")=="triangle":
                    r=inr
            else:
                #trapezoid
                theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if self.getDim("Tooth Shape")=="triangle":
                theta+=inc/2.0
                r=outr
            else:
                r=inr
                if self.getDim("Tooth Shape")=="trapezoid":
                    theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            #done with triangle
            if self.getDim("Tooth Shape")!="triangle":
                #r is still inr
                if self.getDim("Tooth Shape")=="trapezoid":
                    theta += inc/4.0
                else:
                    theta+=inc/2.0
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
                if self.getDim("Tooth Shape")=="trapezoid":
                    theta+=inc/4.0
                r=outr
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
        if points!=None: points.append(points[0])
        gear.append(plot.PolyLine(points, width=1, legend="gear"))
        #generate bore circle
        bore=self.getDim("Bore Diameter")/2 #convert diameter to radius
        boreCircle=[]
        binc=math.pi/100
        for theta in drange(0,2*math.pi+binc, binc):
            boreCircle.append((bore*math.cos(theta), bore*math.sin(theta)))
        gear.append(plot.PolyLine(boreCircle, width=1, legend="bore"))

        #TODO: hub info

        self.lines=gear

    def makeEditors(self):
        """Generates buttons, spincontrols, etc. to edit gear parameters"""
    #Standard Gear info-------------------------------------------------------------
        gearBox=wx.Panel(self)#wx.StaticBox(self, -1, 'Gear Dimensions:')
        #number of teeth
        self.gearDim["Number of Teeth"]=fs.FloatSpin(gearBox, pos=(10,10), min_val=0, max_val=100,name="Number of Teeth")
        #pitchDiameter
        self.gearDim["Pitch Diameter"]=fs.FloatSpin(gearBox,pos=(10,10), min_val=0, max_val=10,name="Pitch Diameter")
        #Thickness
        self.gearDim["Thickness"]=fs.FloatSpin(gearBox,pos=(10,10), min_val=0, max_val=10,name="Thickness")
        #Bore Diameter
        self.gearDim["Bore Diameter"]=fs.FloatSpin(gearBox,pos=(10,10), min_val=0, max_val=10,name="Bore Diameter")
        #tooth shape
        self.gearDim["Tooth Shape"]=wx.TextCtrl(gearBox,pos=(10,10), value="Triangle", name="Tooth Shape")#test only, will be radio buttons or list


        gearBoxSizer=wx.GridSizer(len(self.gearDim),2,4,4)
        for dim in self.gearDim:
            gearBoxSizer.Add(wx.StaticText(gearBox,-1, self.gearDim[dim].GetName()))
            gearBoxSizer.Add(self.gearDim[dim])
        gearBox.SetSizer(gearBoxSizer)

        #Hub info-------------------------------------------------------------
        hubBox=wx.Panel(self)#wx.StaticBox(self, -1, 'Hub Dimensions:')
        hubBoxSizer=wx.GridSizer(len(self.hubDim),2,4,4)

        #Thickness
        self.hubDim["Thickness"]=fs.FloatSpin(hubBox,min_val=0, max_val=10,name="Thickness")
        #Bore Diameter
        self.hubDim["Hub Diameter"]=fs.FloatSpin(hubBox,min_val=0, max_val=10, name="Hub Diameter")

        for dim in self.hubDim:
            hubBoxSizer.Add(wx.StaticText(hubBox,-1, self.hubDim[dim].GetName()))
            hubBoxSizer.Add(self.hubDim[dim])
        hubBox.SetSizer(hubBoxSizer)
        #TODO: Implement keyway option


        return (gearBox, hubBox)



#----------------------------------------------------------------------------------
def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=GearTemplate(frm)
    sizer.Add(panel)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
