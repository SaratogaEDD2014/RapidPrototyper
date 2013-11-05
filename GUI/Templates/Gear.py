#Scott Krulcik 10/29

import PartTemplate
import util.labeledEditors as lbl
import math


class Gear(PartTemplate.PartTemplate):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, pitchDistance=.15, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="triangle"):
        super(Gear, self).__init__()
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.dimensionEditor=gearDimensionEditor(parent)
        self.gearDim["teeth"].SetValue(numTeeth)
        self.gearDim["pitchDiameter"].SetValue(pitchDiameter)
        self.gearDim["bore"].SetValue(bore)
        self.gearDim["thickness"].SetValue(thickness)
        self.gearDim["shape"].SetValue(shape)

        self.hubDim["thickness"].SetValue(hubThickness)
        self.hubDim["diameter"].SetValue(hubDiameter)

    def getDim(self, key):
        if key in seld.gearDim:
            return self.gearDim[name].GetValue()
        else:
            return None

    def getHubDim(self, key):
        if key in seld.hubDim:
            return self.hubDim[name].GetValue()
        else:
            return None

    def setDim(self, key, val):
        if key in seld.gearDim:
            self.gearDim[name].SetValue(val)
        else:
            pass

    def setHubDim(self, key, val):
        if key in seld.hubDim:
            self.hubDim[name].SetValue(val)
        else:
            pass

    def getLines(self):
        pitch = getDim("numTeeth")/detDim("pitchDiameter")
        addendum = 1 /  pitch
        dedendum = 1.157 / pitch
        inr=(getDim("pitchDiameter")/2.0) - dedendum #inner radius
        outr=(getDim("pitchDiameter")/2.0) + addendum #outer radius
        inc=2*math.pi/getDim("numTeeth")
        gear=[]
        for theta in drange(0, 2*math.pi, inc):
            points=[]
            r=outr
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if getDim("shape")!="trapezoid":
                #for rect and tri
                theta+=inc/2.0
                if getDim("shape")=="triangle":
                    r=inr
            else:
                #trapezoid
                theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            if getDim("shape")=="triangle":
                theta+=inc/2.0
                r=outr
            else:
                r=inr
                if getDim("shape")=="trapezoid":
                    theta+=inc/4.0
            points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            #done with triangle
            if getDim("shape")!="triangle":
                #r is still inr
                if getDim("shape")=="trapezoid":
                    theta += inc/4.0
                else:
                    theta+=inc/2.0
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
                if getDim("shape")=="trapezoid":
                    theta+=inc/4.0
                r=outr
                points.append([r*trig(theta) for trig in [math.cos, math.sin]])
            gear.append(plot.PolyLine(points))
        #add stuff to hub
        return gear

def gearDimensionEditor(parent):
    viewPanel=wx.Panel(parent)

#Standard Gear info-------------------------------------------------------------
    #number of teeth
    self.gearDim["teeth"]=lbl.LabeledSpin(viewPanel, name="Number of teeth:", max=100)
    #pitchDiameter
    self.gearDim["pitchDiameter"]=lbl.LabeledSpin(viewPanel, name="Pitch Diameter:", max=10)
    #pitchDistance
    self.gearDim["pitchDistance"]=lbl.LabeledSpin(viewPanel, name="Ammendum:", max=1.0)
    #Thickness
    self.gearDim["thickness"]=lbl.LabeledSpin(viewPanel, name="Thickness:", max=10)
    #Bore Diameter
    self.gearDim["bore"]=lbl.LabeledSpin(viewPanel, name="Bore Diameter:", max=10)

    gearBox=wx.StaticBox(viewPanel, -1, 'Gear Dimensions:')
    gearBoxSizer=wx.BoxSizer(wx.VERTICAL)
    for pan in self.gearDim:
        gearBoxSizer.Add(pan)
    gearBox.SetSizer(gearBoxSizer)

#Hub info-------------------------------------------------------------
    #Hub Diameter
    self.hubDim["diameter"]=lbl.LabeledSpin(viewPanel, name="Diameter:", max=10)
    #Hub Thickness
    self.hubDim["thickness"]=lbl.LabeledSpin(viewPanel, name="Thickness:", max=10)

    hubBox=wx.StaticBox(viewPanel, -1, 'Hub Dimensions:')
    hubBoxSizer=wx.BoxSizer(wx.VERTICAL)
    for pan in self.hubDim:
        hubBoxSizer.Add(pan)
    hubBox.SetSizer(gearBoxSizer)
    #Implement keyway afterwards

    viewSizer=wx.BoxSizer(wx.VERTICAL)
    viewSizer.Add(gearBox)
    viewSizer.Add(hubBox)
    viewPanel.SetSizer(viewSizer)
    return viewPanel

