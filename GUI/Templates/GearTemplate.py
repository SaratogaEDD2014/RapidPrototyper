#-------------------------------------------------------------------------------
# Name:        GearTemplate
# Purpose:     This is a panel for generating a gear. It contains window objects to edit parameters and can return a list of points representing the gear object
#
# Author:      Scott Krulcik
# Created:     11/2013
#-------------------------------------------------------------------------------

#Scott Krulcik 10/29

import math
import wx
import GUI.settings as settings
import GUI.util.plot as plot
import GUI.util.editors as editors
from GUI.util.app_util import DynamicPanel
from GUI.util.convert_stl import *
from GUI.PartViewer import *

shapes=['trapezoid','triangle', 'rectangle','sprocket']

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class GearTemplate(wx.Panel):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="trapezoid"):
        super(GearTemplate, self).__init__(parent, pos=(0,settings.toolbar_h), size=(settings.app_w,settings.app_h))
        self.SetBackgroundColour(wx.Colour(255, 200, 150))#settings.defaultBackground)
        self.Show(False)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.lines=[]
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.file=None

        self.display = plot.PlotCanvas(self, pos=(0,0), size=(self.GetSize()[0]/2, self.GetSize()[1]))
        self.display.SetBackgroundColour(wx.Colour(240,240,240))
        self.edit_panel = wx.Panel(self, pos=(self.GetSize()[0]*5/8, 0), size=(self.GetSize()[0]/2, self.GetSize()[1]))
        self.edit_panel.SetBackgroundColour(wx.Colour(255,0,0))
        self.makeEditors()

        self.setDim("Number of Teeth", numTeeth)
        self.setDim("Pitch Diameter",pitchDiameter)
        self.setDim("Bore Diameter",bore)
        self.setDim("Thickness",thickness)
        self.setDim("Tooth Shape",shape)
        self.setHubDim("Thickness",hubThickness)
        self.setHubDim("Hub Diameter",hubDiameter)
        self.OnUpdate(None)

    def OnSize(self, event):
        event.Skip()
        self.display.SetSize((self.GetSize()[0]/2, self.GetSize()[1]))
        self.edit_panel.SetSize((self.GetSize()[0]/2, self.GetSize()[1]))
        self.edit_panel.SetPosition((self.display.GetSize()[0], 0))

    def OnUpdate(self, event):
        self.makeGear()
        self.grid = plot.PlotGraphics(self.lines, 'Custom Gear')
        self.display.Draw(self.grid)

    def OnPrint(self, event):
        self.generate_vertices(self.rim_circle, self.bore_circle, self.hub_circle)
        part_viewer = STLViewer(settings.main_window, settings.PATH+'examples/temp_file.stl')
        settings.set_view(part_viewer)

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


    def triangle(self, inc, outr, inr):
        #gear teeth
        points=[]
        #generate bore circle
        bore=self.getDim("Bore Diameter")/2.0 #convert diameter to radius
        boreCircle=[]
        #generate hub circle
        hub=self.getHubDim("Hub Diameter")/2.0 #convert diameter to radius
        hubCircle=[]
        points.append([outr*trig(0) for trig in [math.cos, math.sin]])
        boreCircle.append([bore*trig(0) for trig in [math.cos, math.sin]])
        hubCircle.append([hub*trig(0) for trig in [math.cos, math.sin]])

        for theta in drange(0, 2*math.pi, inc):
            theta+=inc/2.0
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=inc/2.0
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
        if points!=None: points.append(points[0])
        plotlines= [plot.PolyLine(points, width=1, legend="gear")]
        plotlines.append(plot.PolyLine(boreCircle, width=1, legend="bore"))
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=settings.defaultAccent))
        return plotlines

    def rectangle(self, inc, outr, inr):
        #gear teeth
        points=[]
        #generate bore circle
        bore=self.getDim("Bore Diameter")/2.0 #convert diameter to radius
        boreCircle=[]
        #generate hub circle
        hub=self.getHubDim("Hub Diameter")/2.0 #convert diameter to radius
        hubCircle=[]

        points.append([outr*trig(0) for trig in [math.cos, math.sin]])
        boreCircle.append([bore*trig(0) for trig in [math.cos, math.sin]])
        hubCircle.append([hub*trig(0) for trig in [math.cos, math.sin]])

        for theta in drange(0, 2*math.pi, inc):
            theta+=inc/2.0
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=inc/2.0
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])

        if points!=None: points.append(points[0])
        plotlines= [plot.PolyLine(points, width=1, legend="gear")]
        plotlines.append(plot.PolyLine(boreCircle, width=1, legend="bore"))
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=settings.defaultAccent))
        return plotlines

    def trapezoid(self, inc, outr, inr):
        #gear teeth
        points=[]
        #generate bore circle
        bore=self.getDim("Bore Diameter")/2.0 #convert diameter to radius
        boreCircle=[]
        #generate hub circle
        hub=self.getHubDim("Hub Diameter")/2.0 #convert diameter to radius
        hubCircle=[]
        points.append([outr*trig(0) for trig in [math.cos, math.sin]])
        boreCircle.append([bore*trig(0) for trig in [math.cos, math.sin]])
        hubCircle.append([hub*trig(0) for trig in [math.cos, math.sin]])

        for theta in drange(0, 2*math.pi, inc):
            theta+=inc/4
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=inc/4
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=inc/4
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=inc/4
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
        if points!=None: points.append(points[0])
        self.rim_circle = points
        self.bore_circle = boreCircle
        self.hub_circle = hubCircle
        plotlines= [plot.PolyLine(points, width=1, legend="gear")]
        plotlines.append(plot.PolyLine(boreCircle, width=1, legend="bore"))
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=settings.defaultAccent))
        return plotlines

    def sprocket(self, inc, outr, inr):
        points=[]
        points.append([outr*trig(0) for trig in [math.cos, math.sin]])
        for theta in drange(0, 2*math.pi, inc):
            theta+=5*inc/16
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=3*inc/16
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=5*inc/16
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            theta+=3*inc/16
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
            hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
        #if points!=None: points+=points[0:3]
        return [plot.PolySpline(points, width=1, legend="gear")]



    def makeGear(self):
        pitch = self.getDim("Number of Teeth")/self.getDim("Pitch Diameter")
        addendum = 1.0 /  pitch
        dedendum = 1.157 / pitch
        inr=(self.getDim("Pitch Diameter")/2.0) - dedendum #inner radius
        outr=(self.getDim("Pitch Diameter")/2.0) + addendum #outer radius
        inc=2*math.pi/self.getDim("Number of Teeth")

        gear=[]
        shapeFunctions={"triangle":self.triangle, "rectangle":self.rectangle, "trapezoid":self.trapezoid, "sprocket":self.sprocket}
        polyshapes = shapeFunctions[self.getDim("Tooth Shape")](inc, outr, inr)

        for line in polyshapes:
            gear.append(line)
        self.lines=gear

    def makeEditors(self):
        """Generates buttons, spincontrols, etc. to edit gear parameters"""
        elements = []
    #Standard Gear info-------------------------------------------------------------
        #number of teeth
        self.gearDim["Number of Teeth"]=editors.TouchSpin(self.edit_panel, limits=(0,100), increment=1,name="Number of Teeth")
        self.gearDim["Number of Teeth"].SetPrecision(0)
        #pitchDiameter
        self.gearDim["Pitch Diameter"]=editors.TouchSpin(self.edit_panel,limits=(0,10),increment=0.05, name="Pitch Diameter")
        self.gearDim["Pitch Diameter"].SetPrecision(3)
        #Thickness
        self.gearDim["Thickness"]=editors.TouchSpin(self.edit_panel,limits=(0,10),increment=0.05,name="Thickness")
        self.gearDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.gearDim["Bore Diameter"]=editors.TouchSpin(self.edit_panel,limits=(0,10),increment=0.05,name="Bore Diameter")
        self.gearDim["Bore Diameter"].SetPrecision(3)
        #tooth shape
        self.gearDim["Tooth Shape"]=wx.ComboBox(self.edit_panel, value=shapes[0], choices=shapes, name="Tooth Shape")


        for dim in self.gearDim:
            #temp = wx.Panel(self.edit_panel)
            #text = wx.StaticText(temp, -1, self.gearDim[dim].GetName()+":")
            #text.SetForegroundColour(wx.Colour(255,255,255))
            #text.SetBackgroundColour(self.GetBackgroundColour())
            #temp_sizer = wx.GridSizer(1,2,10,10)
            #temp_sizer.Add(text, flag=wx.EXPAND)
            #temp_sizer.Add(self.gearDim[dim])
            #temp.SetSizer(temp_sizer)
            #elements.append(temp)
            elements.append(self.gearDim[dim])

        #Hub info-------------------------------------------------------------
        #Thickness
        self.hubDim["Thickness"]=editors.TouchSpin(self.edit_panel,limits=(0,10),increment=0.05,name="Thickness")
        self.hubDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.hubDim["Hub Diameter"]=editors.TouchSpin(self.edit_panel,limits=(0,10),increment=0.05, name="Hub Diameter")
        self.hubDim["Hub Diameter"].SetPrecision(3)

        for dim in self.hubDim:
            #temp = wx.Panel(self.edit_panel)
            #text = wx.StaticText(temp, -1, self.hubDim[dim].GetName()+":")
            #text.SetForegroundColour(wx.Colour(255,255,255))
            #text.SetBackgroundColour(self.GetBackgroundColour())
            #temp_sizer = wx.GridSizer(1,2,10,10)
            #temp_sizer.Add(text, flag=wx.EXPAND)
            #temp_sizer.Add(self.hubDim[dim])
            #temp.SetSizer(temp_sizer)
            #elements.append(temp)
            elements.append(self.hubDim[dim])

        #TODO: Implement keyway option
        self.updateButton = wx.Button(self, 1, 'Update')
        self.print_button = wx.Button(self, 2, 'Print')
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnPrint, id=2)
        button_sizer = wx.GridSizer(1,2,5, self.edit_panel.GetSize()[0]/80)
        button_sizer.Add(self.updateButton)
        button_sizer.Add(self.print_button)
        butt_panel = wx.Panel(self.edit_panel)
        butt_panel.SetSizer(button_sizer)
        elements.append(butt_panel)

        self.edit_panel.elements = elements

    def generate_vertices(self, points, bore, hub):
        self.file=open(settings.PATH+'examples/temp_file.stl','w')
        self.add_to_stl("solid shape")
        thickness=self.getDim("Thickness")
        hub_thick=self.getHubDim("Thickness")

        for i in range(0, len(points)-2):
            p1 = points[i][:] + [0.0]
            p2 = points[i+1][:] + [0.0]
            p3 = p1[:2] + [thickness]
            p4 = p2[:2] +[thickness]
            c1 = bore[i][:] + [0.0]
            c2 = bore[i+1][:] + [0.0]
            c3 = bore[i][:] + [thickness]
            c4 = bore[i+1][:] + [thickness]
            c5 = c3[:2]+[thickness + hub_thick]
            c6 = c4[:2]+[thickness + hub_thick]
            h1 = hub[i][:] + [0.0]
            h2 = hub[i+1][:] + [0.0]
            h3 = h1[:2] + [thickness + hub_thick]
            h4 = h2[:2] + [thickness + hub_thick]

            normal = [0.0,0.0,-1.0]#point down
            a1=p1[:]
            a2=p2[:]
            #self.print_facet(center, p2, p1, normal)
            self.print_rect_facets(p1, c1, c2, p2, normal)

            normal = [0.0, 0.0, 1.0] #point up
            a3 = p3[:]
            a4 = p4[:]
            self.print_rect_facets(a3, a4, c4, c3, normal)
            self.print_rect_facets(h3, h4, c6, c5, normal)


            normal = [a2[0]-a1[0], a2[1]-a1[1], 0.0]
            self.print_rect_facets(a1, a2, a4, a3, normal)

            normal = [c1[0]-c2[0], c1[1]-c2[1], 0.0]
            self.print_rect_facets(c3, c4, c2, c1, normal)
            self.print_rect_facets(c5, c6, c4, c3, normal)

            normal = [h2[0]-h1[0], h2[1]-h1[1], 0.0]
            self.print_rect_facets(h1, h2, h4, h3, normal)
        self.add_to_stl("endsolid")
        self.file.close()


    def print_facet(self, p1,p2,p3, vector):
        self.add_to_stl('facet normal '+ self.point_as_string(vector))
        self.add_to_stl('  outer loop')
        self.add_to_stl('    vertex ' + self.point_as_string(p1))
        self.add_to_stl('    vertex ' + self.point_as_string(p2))
        self.add_to_stl('    vertex ' + self.point_as_string(p3))
        self.add_to_stl('  endloop')
        self.add_to_stl('endfacet')

    def print_rect_facets(self, p1, p2, p3, p4, vector):
        #first tri: a1-a2-a3
        #second tri: a2-a4-a3
        self.print_facet(p1, p2, p3, vector)
        self.print_facet(p1, p3, p4, vector)

    def point_as_string(self, p):
        strings=str(p[0])+' '+str(p[1])+' '+str(p[2])
        return strings
    def add_to_stl(self, stuff):
        self.file.write(stuff+'\n')



#----------------------------------------------------------------------------------
def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', pos=(0,0), size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=GearTemplate(frm)
    sizer.Add(panel, flag=wx.EXPAND)
    panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
