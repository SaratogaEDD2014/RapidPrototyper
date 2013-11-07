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
import util.plot as plot
import wx.lib.agw.floatspin as fs

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class Gear(wx.Panel):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="triangle"):
        super(Gear, self).__init__()
        self.Show(False)
        self.lines=lines
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.AddEditors()
        self.dimensionEditor=self.generateGearDimensionEditor(parent)
        self.gearDim["numTeeth"].SetValue(numTeeth)
        self.gearDim["pitchDiameter"].SetValue(pitchDiameter)
        self.gearDim["bore"].SetValue(bore)
        self.gearDim["thickness"].SetValue(thickness)
        self.gearDim["shape"].SetValue(shape)

        self.hubDim["thickness"].SetValue(hubThickness)
        self.hubDim["diameter"].SetValue(hubDiameter)
        self.makeGear()


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

    #Standard Gear info-------------------------------------------------------------
        #number of teeth
        wx.StaticText(self, label="Number of teeth:")
        self.gearDim["numTeeth"]=fs.FloatSpin(viewPanel,min_val=0, max_val=100)
        #pitchDiameter
        wx.StaticText(self, label="Pitch Diameter:")
        self.gearDim["pitchDiameter"]=fs.FloatSpin(viewPanel,min_val=0, max_val=10)
        #Thickness
        wx.StaticText(self, label="Thickness:")
        self.gearDim["thickness"]=fs.FloatSpin(viewPanel,min_val=0, max_val=10)
        #Bore Diameter
        wx.StaticText(self, label="Bore Diameter:")
        self.gearDim["bore"]=fs.FloatSpin(viewPanel,min_val=0, max_val=10)
        #tooth shape
        wx.StaticText(self, label="Tooth Shape:")
        self.gearDim["shape"]=wx.TextCtrl(viewPanel, value="Tooth Shape:")#test only, will be radio buttons or list

        gearBox=wx.StaticBox(viewPanel, -1, 'Gear Dimensions:')
        gearBoxSizer=wx.BoxSizer(wx.VERTICAL)
        for dim in self.gearDim:
            gearBoxSizer.Add(self.gearDim[dim])
        gearBox.SetSizer(gearBoxSizer)

    #Hub info-------------------------------------------------------------
        hubBox=wx.StaticBox(viewPanel, -1, 'Hub Dimensions:')
        hubBoxSizer=wx.BoxSizer(wx.VERTICAL)

        #Thickness
        wx.StaticText(self, label="Thickness:")
        self.gearDim["thickness"]=fs.FloatSpin(viewPanel,min_val=0, max_val=10)
        #Bore Diameter
        wx.StaticText(self, label="Bore Diameter:")
        self.hubDim["diameter"]=fs.FloatSpin(viewPanel,min_val=0, max_val=10)

        for dim in self.hubDim:
            hubBoxSizer.Add(self.hubDim[dim])
        hubBox.SetSizer(gearBoxSizer)
        #Implement keyway afterwards

        viewSizer=wx.BoxSizer(wx.VERTICAL)
        viewSizer.Add(gearBox)
        viewSizer.Add(hubBox)
        self.SetSizer(viewSizer)