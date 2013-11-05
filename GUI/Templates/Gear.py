#Scott Krulcik 10/29

import PartTemplate from PartTemplate
import util.labeledEditors as lbl
import math

def tri(g):
    return trap(data)#testing only

def trap(g):
    line1=[(1,2),(2,4),(3,9),(4,16),(5,25)]
    line2=[(-4,3),(-3,3),(-2,2),(-1,2),(0,3)]
    line3=[(1,3),(2,2),(3,2),(4,3),(5,3)]
    return (line1, line2, line3)#testing only

def rect(g):
    return trap(data)#testing only


shapes={"triangle":tri, "trapezoid":trap, "rectangle":rect}

class Gear(PartTemplate):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, pitchDistance=.15, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="triangle"):
        super(Gear, self).__init__()
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.dimensionEditor=gearDimensionEditor(parent)
        self.gearDim["teeth"].SetValue(numTeeth)
        self.gearDim["pitchDiameter"].SetValue(pitchDiameter)
        self.gearDim["pitchDistance"].SetValue(pitchDistance)
        self.gearDim["bore"].SetValue(bore)
        self.gearDim["thickness"].SetValue(thickness)
        
        self.hubDim["thickness"].SetValue(hubThickness)
        self.hubDim["diameter"].SetValue(hubDiameter)
        
        self.shape=shape

    def getData(self):
        global shapes
        if(!shapes.has_key(self.shape)):
            self.shape="triangle"
        return shapes[self.shape](self)

    def getDim(self, key):
        if key in seld.gearDim:
            return self.gearDim[name].GetValue()
        else return None
            
    def getHubDim(self, key):
        if key in seld.hubDim:
            return self.hubDim[name].GetValue()
        else return None

    def setDim(self, key, val):
        if key in seld.gearDim:
            self.gearDim[name].SetValue(val)
        else pass

    def setHubDim(self, key, val):
        if key in seld.hubDim:
            self.hubDim[name].SetValue(val)
        else pass


    def getShape(self):
        return self.shape
    def setShape(self, value):
        self.shape = value

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

