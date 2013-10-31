#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      scott Krulcik
#
# Created:     24/10/2013
#-------------------------------------------------------------------------------
import wx
import wx.lib.plot as plot
import AppSettings
import numpy

class TemplateEditor(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        super(TemplateEditor, self).__init__(parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(AppSettings.defaultBackground)
        wx.StaticText(self, -1, 'Pitch Diameter:', (20, 20))
        self.sc0 = wx.SpinCtrl(self, -1, str(0), (80, 15), (60, -1))
        wx.StaticText(self, -1, 'Number of Teeth:', (20, 70))
        self.sc1 = wx.SpinCtrl(self, -1, str(0), (80, 15), (60, -1))
        wx.StaticText(self, -1, 'Bore Diameter', (20,70))
        self.sc2 = wx.SpinCtrl(self, -1, str(0), (80, 65), (60, -1))
        wx.Button(self, 1, 'Update', (20, 120))

        DrawingView(self)

        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=1)
        self.Centre()

    def OnUpdate(self, event):
        print("Pitch Diameter: ", self.sc0.GetValue())
        print("Number of Teeth", self.sc1.GetValue())
        print("Bore Diameter", self.sc2.GetValue())

class DrawingView(plot.PlotCanvas):
    def __init__(self, parent, lines=[plot.PolyLine([(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]),plot.PolyLine([(-4,2), (-2,3), (-1,5), (1,8), (2,8), (4,10)])]):
        super(DrawingView, self).__init__(parent)
        self.lines=lines
    #self.Bind(wx.EVT_BUTTON, self.draw, id=2)

    """def defaultDraw(self, event):
        gc = plot.PlotGraphics(self.lines, 'Gear')
        self.Draw(gc,  xAxis= (0,15), yAxis= (0,15))"""







#-----------------------------------------------------------------------
if __name__ == '__main__':
    def _InitObjects():
        # 100 points sin function, plotted as green circles
        data1 = 2.*numpy.pi*numpy.arange(200)/200.
        data1.shape = (100, 2)
        data1[:,1] = numpy.sin(data1[:,0])
        markers1 = plot.PolyMarker(data1, colour='green', marker='circle',size=1)
        
        # 50 points cos function, plotted as red line
        data1 = 2.*numpy.pi*numpy.arange(100)/100.
        data1.shape = (50,2)
        data1[:,1] = numpy.cos(data1[:,0])
        lines = plot.PolyLine(data1, colour='red')
        
        # A few more points...
        pi = numpy.pi
        markers2 = plot.PolyMarker([(0., 0.), (pi/4., 1.), (pi/2, 0.),
                               (3.*pi/4., -1)], colour='blue',
                              fillcolour='green', marker='cross')
                              
        return plot.PlotGraphics([markers1, lines, markers2])
    
    
    class AppFrame(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title,
            wx.DefaultPosition, (400, 400))

            # Now Create the menu bar and items
            self.mainmenu = wx.MenuBar()

            menu = wx.Menu()
            menu.Append(200, '&Print...', 'Print the current plot')
            self.Bind(wx.EVT_MENU, self.OnFilePrint, id=200)
            menu.Append(209, 'E&xit', 'Enough of this already!')
            self.Bind(wx.EVT_MENU, self.OnFileExit, id=209)
            self.mainmenu.Append(menu, '&File')

            menu = wx.Menu()
            menu.Append(210, '&Draw', 'Draw plots')
            self.Bind(wx.EVT_MENU,self.OnPlotDraw, id=210)
            menu.Append(211, '&Redraw', 'Redraw plots')
            self.Bind(wx.EVT_MENU,self.OnPlotRedraw, id=211)
            menu.Append(212, '&Clear', 'Clear canvas')
            self.Bind(wx.EVT_MENU,self.OnPlotClear, id=212)
            self.mainmenu.Append(menu, '&Plot')

            menu = wx.Menu()
            menu.Append(220, '&About', 'About this thing...')
            self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=220)
            self.mainmenu.Append(menu, '&Help')

            self.SetMenuBar(self.mainmenu)

            # A status bar to tell people what's happening
            self.CreateStatusBar(1)
            self.testPanel=wx.Panel(self, pos=(400,400))
            self.testPanel.SetBackgroundColour(wx.Colour(200,0,0))
            self.client = DrawingView(self)
        
        def OnFilePrint(self, event):
            d = wx.MessageDialog(self,
                                 """As of this writing, printing support in wxPython is shaky at best.
                                     Are you sure you want to do this?""", "Danger!", wx.YES_NO)
            if d.ShowModal() == wx.ID_YES:
                psdc = wx.PostScriptDC("out.ps", True, self)
                self.client.redraw(psdc)
        
        def OnFileExit(self, event):
            self.Close()
        
        def OnPlotDraw(self, event):
            self.client.Draw(_InitObjects(),'automatic','automatic');
        
        def OnPlotRedraw(self,event):
            self.client.redraw()
        
        def OnPlotClear(self,event):
            self.client.last_draw = None
            dc = wx.ClientDC(self.client)
            dc.Clear()
        
        def OnHelpAbout(self, event):
            about = wx.MessageDialog(self, __doc__, "About...", wx.OK)
            about.ShowModal()
    
    
    
    class MyApp(wx.App):
        def OnInit(self):
            frame = AppFrame(None, -1, "wxPlotCanvas")
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    
    
    app = MyApp(0)
    app.MainLoop()




#----------------------------------------------------------------------------