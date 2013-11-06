#Scott Krulcik 10/29

import PartTemplate
import GUI.util.labeledEditors as lbl
import math
import wx
import util.plot as plot

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class Gear(PartTemplate.PartTemplate):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="triangle"):
        super(Gear, self).__init__()
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.dimensionEditor=self.generateGearDimensionEditor(parent)
        self.gearDim["numTeeth"].SetValue(numTeeth)
        self.gearDim["pitchDiameter"].SetValue(pitchDiameter)
        self.gearDim["bore"].SetValue(bore)
        self.gearDim["thickness"].SetValue(thickness)
        self.gearDim["shape"].SetValue(shape)

        self.hubDim["thickness"].SetValue(hubThickness)
        self.hubDim["diameter"].SetValue(hubDiameter)
        self.makeGear()

    def getGearDimensionEditor(self):
        return self.dimensionEditor

    def getDim(self, key):
        if key in self.gearDim:
            return self.gearDim[key].GetValue()
        else:
            return None

    def getHubDim(self, key):
        if key in seld.hubDim:
            return self.hubDim[key].GetValue()
        else:
            return None

    def setDim(self, key, val):
        if key in seld.gearDim:
            self.gearDim[key].SetValue(val)
        else:
            pass

    def setHubDim(self, key, val):
        if key in seld.hubDim:
            self.hubDim[key].SetValue(val)
        else:
            pass

    def makeGear(self):
        pitch = self.getDim("numTeeth")/self.getDim("pitchDiameter")
        addendum = 1 /  pitch
        dedendum = 1.157 / pitch
        inr=(self.getDim("pitchDiameter")/2.0) - dedendum #inner radius
        outr=(self.getDim("pitchDiameter")/2.0) + addendum #outer radius
        inc=2*math.pi/self.getDim("numTeeth")
        gear=[]
        for theta in drange(0, 2*math.pi, inc):
            points=[]
            r=outr
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if self.getDim("shape")!="trapezoid":
                #for rect and tri
                theta+=inc/2.0
                if self.getDim("shape")=="triangle":
                    r=inr
            else:
                #trapezoid
                theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if self.getDim("shape")=="triangle":
                theta+=inc/2.0
                r=outr
            else:
                r=inr
                if self.getDim("shape")=="trapezoid":
                    theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            #done with triangle
            if self.getDim("shape")!="triangle":
                #r is still inr
                if self.getDim("shape")=="trapezoid":
                    theta += inc/4.0
                else:
                    theta+=inc/2.0
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
                if self.getDim("shape")=="trapezoid":
                    theta+=inc/4.0
                r=outr
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            gear.append(plot.PolyLine(points))

        #generate bore circle
        bore=self.getDim("bore")/2 #convert diameter to radius
        boreCircle=[]
        for theta in drange(0,2*math.pi, bore*math.pi/100):
            boreCircle.append((round(bore*math.cos(theta),4), round(bore*math.sin(theta),4)))
        gear.append(plot.PolyLine(boreCircle))

        #add stuff to hub
        self.lines=gear

    def generateGearDimensionEditor(self, parent):
        viewPanel=wx.Panel(parent)

    #Standard Gear info-------------------------------------------------------------
        #number of teeth
        self.gearDim["numTeeth"]=lbl.LabeledSpin(viewPanel, name="Number of teeth:", max=100)
        #pitchDiameter
        self.gearDim["pitchDiameter"]=lbl.LabeledSpin(viewPanel, name="Pitch Diameter:", max=10)
        #Thickness
        self.gearDim["thickness"]=lbl.LabeledSpin(viewPanel, name="Thickness:", max=10)
        #Bore Diameter
        self.gearDim["bore"]=lbl.LabeledSpin(viewPanel, name="Bore Diameter:", max=10)
        #tooth shape
        self.gearDim["shape"]=wx.TextCtrl(viewPanel, name="Tooth Shape:")#test only, will be radio buttons or list

        gearBox=wx.StaticBox(viewPanel, -1, 'Gear Dimensions:')
        gearBoxSizer=wx.BoxSizer(wx.VERTICAL)
        for dim in self.gearDim:
            gearBoxSizer.Add(self.gearDim[dim])
        gearBox.SetSizer(gearBoxSizer)

    #Hub info-------------------------------------------------------------
        #Hub Diameter
        self.hubDim["diameter"]=lbl.LabeledSpin(viewPanel, name="Diameter:", max=10)
        #Hub Thickness
        self.hubDim["thickness"]=lbl.LabeledSpin(viewPanel, name="Thickness:", max=10)

        hubBox=wx.StaticBox(viewPanel, -1, 'Hub Dimensions:')
        hubBoxSizer=wx.BoxSizer(wx.VERTICAL)
        for dim in self.hubDim:
            hubBoxSizer.Add(self.hubDim[dim])
        hubBox.SetSizer(gearBoxSizer)
        #Implement keyway afterwards

        viewSizer=wx.BoxSizer(wx.VERTICAL)
        viewSizer.Add(gearBox)
        viewSizer.Add(hubBox)
        viewPanel.SetSizer(viewSizer)
        return viewPanel

