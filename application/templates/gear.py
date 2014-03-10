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
import application.settings as settings
import application.util.plot as plot
import application.util.editors as editors
import application.util.app_util as app_util
from numpy import *
from application.util.convert_stl import *
from application.part_viewer import *
from application.bubble_menu import DynamicButtonRect

shapes=['trapezoid','triangle', 'rectangle','sprocket']

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class GearTemplate(wx.Panel):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="trapezoid"):
        super(GearTemplate, self).__init__(parent, pos=(0,40), size=(settings.app_w,settings.app_h-50))
        self.SetBackgroundColour(settings.defaultForeground)
        self.Show(False)
        self.lines=[]
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.file=None

        self.edit = wx.Panel(self)
        self.makeEditors()
        self.setDim("Number of Teeth", numTeeth)
        self.setDim("Pitch Diameter",pitchDiameter)
        self.setDim("Bore Diameter",bore)
        self.setDim("Thickness",thickness)
        self.setDim("Tooth Shape",shape)
        self.setHubDim("Thickness",hubThickness)
        self.setHubDim("Hub Diameter",hubDiameter)

        self.display= plot.PlotCanvas(self, pos=wx.DefaultPosition, size=((settings.app_w*2)/3,settings.app_h-50))
        self.display.SetBackgroundColour(settings.defaultBackground)
        self.display.SetForegroundColour(settings.defaultForeground)
        self.display.SetGridColour(settings.defaultForeground)

        masterSizer=wx.GridSizer(1,2,0,self.GetSize()[0]/60)
        masterSizer.Add(self.display, flag=wx.EXPAND)
        masterSizer.Add(self.edit, flag=wx.EXPAND)
        self.SetSizer(masterSizer)
        self.OnUpdate(None)

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
        plotlines= [plot.PolyLine(points, width=3, legend="gear", colour=settings.defaultForeground)]
        plotlines.append(plot.PolyLine(boreCircle, width=3, legend="bore", colour=settings.defaultForeground))
        plotlines.append(plot.PolyLine(hubCircle, width=3, legend="hub", colour=settings.defaultAccent))
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
        plotlines= [plot.PolyLine(points, width=3, legend="gear", colour=settings.defaultForeground)]
        plotlines.append(plot.PolyLine(boreCircle, width=3, legend="bore", colour=settings.defaultForeground))
        plotlines.append(plot.PolyLine(hubCircle, width=3, legend="hub", colour=settings.defaultAccent))
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

        if bore > 0.0:
            if hub >= bore:
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
            else:
                #A hub inside a bore us meaningless, so don't calculate it
                points.append([outr*trig(0) for trig in [math.cos, math.sin]])
                boreCircle.append([bore*trig(0) for trig in [math.cos, math.sin]])
                for theta in drange(0, 2*math.pi, inc):
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
                    boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
                    boreCircle.append([bore*trig(theta) for trig in [math.cos, math.sin]])
        else:
            #There is no bore
            if hub >= 0.0:
                #There is still a hub, to mill or something
                points.append([outr*trig(0) for trig in [math.cos, math.sin]])
                boreCircle.append([bore*trig(0) for trig in [math.cos, math.sin]])
                hubCircle.append([hub*trig(0) for trig in [math.cos, math.sin]])
                for theta in drange(0, 2*math.pi, inc):
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
                    hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
                    hubCircle.append([hub*trig(theta) for trig in [math.cos, math.sin]])
            else:
                #hub and bore are both not existent
                points.append([outr*trig(0) for trig in [math.cos, math.sin]])
                for theta in drange(0, 2*math.pi, inc):
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
                    theta+=inc/4
                    points.append([outr*trig(theta) for trig in [math.cos, math.sin]])

        if points!=None: points.append(points[0])
        self.rim_circle = points
        self.bore_circle = boreCircle
        self.hub_circle = hubCircle
        plotlines= [plot.PolyLine(points, width=3, legend="gear", colour=settings.defaultForeground)]
        plotlines.append(plot.PolyLine(boreCircle, width=3, legend="bore", colour=settings.defaultForeground))
        plotlines.append(plot.PolyLine(hubCircle, width=3, legend="hub", colour=settings.defaultAccent))
        return plotlines

    def sprocket(self, inc, outr, inr):
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
        plotlines= [plot.PolySpline(points, width=3, legend="gear", colour=settings.defaultForeground)]
        plotlines.append(plot.PolyLine(boreCircle, width=3, legend="bore", colour=settings.defaultForeground))
        plotlines.append(plot.PolyLine(hubCircle, width=3, legend="hub", colour=settings.defaultAccent))
        return plotlines

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
        w,h = self.GetSize()
        edit_panel = wx.Panel(self)
        edit_panel.SetBackgroundColour(self.GetBackgroundColour())
        edit_sizer = wx.GridSizer(0,1, h/60)
        buff1 = wx.Panel(edit_panel)
        buff2 = wx.Panel(edit_panel)
        edit_sizer.Add(buff1)

        #Standard Gear info-------------------------------------------------------------
        gear_title = app_util.TitleBreak(edit_panel, label="Gear Dimensions", color=settings.defaultBackground)
        edit_sizer.Add(gear_title, flag=wx.EXPAND)
        #number of teeth
        self.gearDim["Number of Teeth"]=editors.DimensionEditor(edit_panel, limits=(0,100), increment=1,name="Number of Teeth")
        self.gearDim["Number of Teeth"].SetPrecision(0)
        #pitchDiameter
        self.gearDim["Pitch Diameter"]=editors.DimensionEditor(edit_panel,limits=(0,10),increment=0.05, name="Pitch Diameter")
        self.gearDim["Pitch Diameter"].SetPrecision(3)
        #Thickness
        self.gearDim["Thickness"]=editors.DimensionEditor(edit_panel,limits=(0,10),increment=0.05,name="Thickness")
        self.gearDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.gearDim["Bore Diameter"]=editors.DimensionEditor(edit_panel,limits=(0,10),increment=0.05,name="Bore Diameter")
        self.gearDim["Bore Diameter"].SetPrecision(3)
        #tooth shape
        self.gearDim["Tooth Shape"] = editors.DimensionComboBox(edit_panel, value=shapes[0], choices=shapes, name="Tooth Shape")
        for dim in self.gearDim:
            edit_sizer.Add(self.gearDim[dim], flag=wx.EXPAND)

        edit_sizer.AddSpacer(h/40)

        #Hub info-------------------------------------------------------------
        hub_title = app_util.TitleBreak(edit_panel, label="Hub Dimensions", color=settings.defaultBackground)
        edit_sizer.Add(hub_title, flag=wx.EXPAND)
        #Thickness
        self.hubDim["Thickness"]=editors.DimensionEditor(edit_panel,limits=(0,10),increment=0.05,name="Thickness")
        self.hubDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.hubDim["Hub Diameter"]=editors.DimensionEditor(edit_panel,limits=(0,10),increment=0.05, name="Hub Diameter")
        self.hubDim["Hub Diameter"].SetPrecision(3)
        for dim in self.hubDim:
            edit_sizer.Add(self.hubDim[dim], flag=wx.EXPAND)

        edit_sizer.AddSpacer(h/40)


        #Buttons---------------------------------------------------------------
        button_panel = wx.Window(edit_panel, size=(self.GetSize()[0]/2,self.GetSize()[1]/3), pos=(self.GetSize()[0]/2,(self.GetSize()[1]*2)/3))
        button_panel.SetBackgroundColour(settings.defaultForeground)
        inside_color = app_util.dim_color(settings.defaultAccent, -30)
        outside_color = app_util.dim_color(settings.defaultAccent, 20)
        self.updateButton = DynamicButtonRect(button_panel, "Update", inside_color, outside_color, settings.defaultBackground, id=1)
        self.print_button = DynamicButtonRect(button_panel, "Print", inside_color, outside_color, settings.defaultBackground, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnUpdate)
        self.Bind(wx.EVT_BUTTON, self.OnPrint, id=2)
        button_sizer=wx.GridSizer(0,2,30,30)
        button_sizer.Add(self.updateButton, flag=wx.EXPAND)
        button_sizer.Add(self.print_button, flag=wx.EXPAND)
        button_panel.SetSizer(button_sizer)
        edit_sizer.Add(button_panel, flag=wx.EXPAND)

        #TODO: Implement keyway option
        edit_sizer.Add(buff2)
        edit_panel.SetSizer(edit_sizer)
        self.edit = edit_panel

    def generate_vertices(self, points, bore, hub):
        self.file=open(settings.PATH+'examples/temp_file.stl','w')
        self.add_to_stl("solid shape")
        thickness=self.getDim("Thickness")
        hub_thick=self.getHubDim("Thickness")
        if len(bore) == 0:
            #Probable 0 but < gives leeway for other errors
            bore = zeros((len(points), 3)).tolist() #numpy array of zeroes
        if len(hub) == 0:
            hub = bore[:]

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
            h5 = h1[:2] + [thickness]
            h6 = h2[:2] + [thickness]

            normal = [0.0,0.0,-1.0]#point down
            a1=p1[:]
            a2=p2[:]
            self.print_rect_facets(p1, c1, c2, p2, normal)

            normal = [0.0, 0.0, 1.0] #point up
            a3 = p3[:]
            a4 = p4[:]
            #self.print_rect_facets(a3, a4, c4, c3, normal)
            self.print_rect_facets(a3, a4, h6, h5, normal)
            self.print_rect_facets(h3, h4, c6, c5, normal)


            normal = [a2[0]-a1[0], a2[1]-a1[1], 0.0]
            self.print_rect_facets(a1, a2, a4, a3, normal)

            normal = [c1[0]-c2[0], c1[1]-c2[1], 0.0]
            self.print_rect_facets(c3, c4, c2, c1, normal)
            self.print_rect_facets(c5, c6, c4, c3, normal)

            normal = [h2[0]-h1[0], h2[1]-h1[1], 0.0]
            self.print_rect_facets(h5, h6, h4, h3, normal)
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
    frm = wx.Frame(None, -1, 'Gear Display', pos=(0,0), size=(1000,800))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=GearTemplate(frm)
    sizer.Add(panel)
    panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
