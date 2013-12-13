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
import GUI.AppSettings as AppSettings
import GUI.util.plot as plot
import GUI.util.editors as editors

shapes=['trapezoid','triangle', 'rectangle','sprocket']

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

class GearTemplate(wx.Panel):
    def __init__(self, parent, numTeeth=25, pitchDiameter=3.0, bore=1.0, thickness=.25, hubDiameter=0, hubThickness=0, shape="trapezoid"):
        super(GearTemplate, self).__init__(parent, pos=(0,40), size=(800,400))
        self.SetBackgroundColour(AppSettings.defaultBackground)
        self.Show(False)
        self.lines=[]
        self.gearDim={}#dict for standard gear values
        self.hubDim={} #dict for hub dimensions
        self.file=None

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

        self.display= plot.PlotCanvas(self, pos=wx.DefaultPosition, size=(400,400))
        self.display.SetBackgroundColour(wx.Colour(240,240,240))

        masterSizer=wx.BoxSizer(wx.HORIZONTAL)
        editorSizer=wx.BoxSizer(wx.VERTICAL)
        temp=wx.Panel(self, pos=(-20,-20), size=(16,16))
        temp.SetBackgroundColour(self.GetBackgroundColour())
        editorSizer.Add(temp)#spacer
        for e in self.editors:
            editorSizer.Add(e)
            temp=wx.Panel(self, pos=(-20,-20), size=(16,16))
            temp.SetBackgroundColour(self.GetBackgroundColour())
        editorSizer.Add(temp)#spacer
        editorSizer.Add(self.updateButton)
        masterSizer.Add(self.display)
        temp=wx.Panel(self, pos=(-20,-20), size=(16,16))
        temp.SetBackgroundColour(self.GetBackgroundColour())
        masterSizer.Add(temp)#spacer
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
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=AppSettings.defaultAccent))
        self.generate_vertices(points, boreCircle, hubCircle)
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
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=AppSettings.defaultAccent))
        self.generate_vertices(points, boreCircle, hubCircle)
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
        plotlines= [plot.PolyLine(points, width=1, legend="gear")]
        plotlines.append(plot.PolyLine(boreCircle, width=1, legend="bore"))
        plotlines.append(plot.PolyLine(hubCircle, width=1, legend="hub", colour=AppSettings.defaultAccent))
        self.generate_vertices(points, boreCircle, hubCircle)
        return plotlines

    def sprocket(self, inc, outr, inr):
        points=[]
        points.append([outr*trig(0) for trig in [math.cos, math.sin]])
        for theta in drange(0, 2*math.pi, inc):
            theta+=5*inc/16
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
            theta+=3*inc/16
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            theta+=5*inc/16
            points.append([inr*trig(theta) for trig in [math.cos, math.sin]])
            theta+=3*inc/16
            points.append([outr*trig(theta) for trig in [math.cos, math.sin]])
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
        for line in shapeFunctions[self.getDim("Tooth Shape")](inc, outr, inr):
            gear.append(line)
        self.lines=gear

    def makeEditors(self):
        """Generates buttons, spincontrols, etc. to edit gear parameters"""
    #Standard Gear info-------------------------------------------------------------
        gearBox=wx.StaticBox(self, -1, 'Gear Dimensions:')
        gearBox.SetForegroundColour(wx.Colour(255,255,255))
        gearBox.SetBackgroundColour(self.GetBackgroundColour())
        #should improve coloring on linux system
        gearPanel=wx.Panel(self)
        gearPanel.SetBackgroundColour(self.GetBackgroundColour())

        #number of teeth
        self.gearDim["Number of Teeth"]=editors.TouchSpin(gearPanel, limits=(0,100), increment=1,name="Number of Teeth")
        self.gearDim["Number of Teeth"].SetPrecision(0)
        #pitchDiameter
        self.gearDim["Pitch Diameter"]=editors.TouchSpin(gearPanel,limits=(0,10),increment=0.05, name="Pitch Diameter")
        self.gearDim["Pitch Diameter"].SetPrecision(3)
        #Thickness
        self.gearDim["Thickness"]=editors.TouchSpin(gearPanel,limits=(0,10),increment=0.05,name="Thickness")
        self.gearDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.gearDim["Bore Diameter"]=editors.TouchSpin(gearPanel,limits=(0,10),increment=0.05,name="Bore Diameter")
        self.gearDim["Bore Diameter"].SetPrecision(3)
        #tooth shape
        self.gearDim["Tooth Shape"]=wx.ComboBox(gearPanel, value=shapes[0], choices=shapes, name="Tooth Shape")


        gearBoxSizer=wx.GridSizer(len(self.gearDim),2,8,8)
        for dim in self.gearDim:
            temp=wx.StaticText(gearPanel,-1, self.gearDim[dim].GetName()+":", size=(125,-1))
            temp.SetBackgroundColour(gearPanel.GetBackgroundColour())
            temp.SetForegroundColour(wx.Colour(255,255,255))
            gearBoxSizer.Add(temp)
            gearBoxSizer.Add(self.gearDim[dim], flag=wx.ALIGN_RIGHT)
        gearPanel.SetSizer(gearBoxSizer)

        staticSizer=wx.StaticBoxSizer(gearBox)
        staticSizer.Add(gearPanel)

        #Hub info-------------------------------------------------------------
        hubBox=wx.StaticBox(self, -1, 'Hub Dimensions:')
        hubBox.SetForegroundColour(wx.Colour(255,255,255))
        hubBox.SetBackgroundColour(self.GetBackgroundColour())
        hubBoxSizer=wx.GridSizer(len(self.hubDim),2,8,8)
        #better linux coloring
        hubPanel=wx.Panel(self)
        hubPanel.SetBackgroundColour(self.GetBackgroundColour())

        #Thickness
        self.hubDim["Thickness"]=editors.TouchSpin(hubPanel,limits=(0,10),increment=0.05,name="Thickness")
        self.hubDim["Thickness"].SetPrecision(3)
        #Bore Diameter
        self.hubDim["Hub Diameter"]=editors.TouchSpin(hubPanel,limits=(0,10),increment=0.05, name="Hub Diameter")
        self.hubDim["Hub Diameter"].SetPrecision(3)

        for dim in self.hubDim:
            temp=wx.StaticText(hubPanel,-1,self.hubDim[dim].GetName()+":", size=(125,-1))
            temp.SetForegroundColour(wx.Colour(255,255,255))
            temp.SetBackgroundColour(hubPanel.GetBackgroundColour())
            hubBoxSizer.Add(temp)
            hubBoxSizer.Add(self.hubDim[dim], flag=wx.ALIGN_RIGHT)
        hubPanel.SetSizer(hubBoxSizer)

        hubStaticSizer=wx.StaticBoxSizer(hubBox)
        hubStaticSizer.Add(hubPanel)
        #TODO: Implement keyway option


        return (staticSizer, hubStaticSizer)

    def generate_vertices(self, points, bore, hub):
        self.file=open(AppSettings.PATH+'examples/temp_file.stl','w')
        self.add_to_stl("solid shape")
        thickness=self.getDim("Thickness")

        for i in range(0, len(points)-2):
            p1 = points[i][:]+[0]
            p2 = points[i+1][:]+[0]
            c1 = bore[i][:]+[0]
            c2 = bore[i+1][:]+[0]

            p1[2] = 0.0
            p2[2] = 0.0
            c1[2] = 0.0
            c2[2] = 0.0
            #center = [0,0,0]
            #center[2]=0.0
            normal = [0.0,0.0,-1.0]#point down
            a1=p1[:]
            a2=p2[:]
            #self.print_facet(center, p2, p1, normal)
            self.print_rect_facets(p1, c1, p2, c2, normal)

            normal[2] = 1.0 #point up
            p1[2] = thickness
            p2[2] = thickness
            c1[2] = thickness
            c2[2] = thickness
            #center[2] = thickness
            a3 = p1[:]
            a4 = p2[:]
            self.print_rect_facets(p1, c1, p2, c2, normal)

            normal=[a2[0]-a1[0], a2[1]-a1[1], 0.0]
            self.print_rect_facets(a1, a2, a3, a4, normal)

            self.generate_cylinder(bore, thickness, False)

        self.add_to_stl("endsolid")
        self.file.close()

    def generate_cylinder(self, points, thickness, out=True):
        for i in range(0, len(points)-2):
            p1 = points[i][:]+[0.0]
            p2 = points[i+1][:]+[0.0]

            a1=p1[:]
            a2=p2[:]

            p1[2] = thickness
            p2[2] = thickness
            a3 = p1[:]
            a4 = p2[:]

            if out:
                normal=[a2[0]-a1[0], a2[1]-a1[1], 0.0]
            else:
                normal=[a1[0]-a2[0], a1[1]-a2[1], 0.0]
            self.print_rect_facets(a1, a2, a3, a4, normal)


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
        self.print_facet(p2, p4, p3, vector)

    def point_as_string(self, p):
        strings=str(p[0])+' '+str(p[1])+' '+str(p[2])
        return strings
    def add_to_stl(self, stuff):
        self.file.write(stuff+'\n')



#----------------------------------------------------------------------------------
def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=GearTemplate(frm)
    sizer.Add(panel)
    panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
